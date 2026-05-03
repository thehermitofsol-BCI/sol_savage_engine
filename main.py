import os
import base64
import json
import rawpy
import imageio
from flask import Flask, request
from google.cloud import storage, aiplatform
from vertexai.generative_models import GenerativeModel, Image
import psycopg2

app = Flask(__name__)

# --- CONFIGURATION ---
PROJECT_ID = "gen-lang-client-0449364738"
LOCATION = "us-central1"
BUSINESS_NAME = "Sol Savage Enterprise"

# Initialize GCP Clients
storage_client = storage.Client()
aiplatform.init(project=PROJECT_ID, location=LOCATION)
model = GenerativeModel("gemini-1.5-pro-002")

@app.route("/", methods=["POST"])
def process_salvage_photo():
    """
    Triggered by Pub/Sub when a 200MP RAW photo is uploaded to GCS.
    """
    # 1. Parse the incoming event
    envelope = request.get_json()
    if not envelope or "message" not in envelope:
        return "No message received", 400
    
    pubsub_message = envelope["message"]
    data = json.loads(base64.b64decode(pubsub_message["data"]).decode("utf-8"))
    
    bucket_name = data["bucket"]
    file_name = data["name"]
    print(f"Sol Savage Engine: Processing {file_name} from {bucket_name}")

    # 2. Download and Process the 200MP RAW file
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    raw_path = f"/tmp/{file_name}"
    processed_path = "/tmp/processed_preview.jpg"
    
    blob.download_to_filename(raw_path)

    # Convert RAW to RGB for Gemini (200MP to high-quality preview)
    with rawpy.imread(raw_path) as raw:
        # postprocess handles the heavy lifting of the S25 Ultra sensor data
        rgb = raw.postprocess(use_camera_wb=True, no_auto_bright=True, bright=1.0)
        imageio.imsave(processed_path, rgb)

    # 3. Analyze with Gemini Pro 1.5 using NLP/TMS Logic
    with open(processed_path, "rb") as f:
        image_bytes = f.read()

    # WORLD-CLASS SYSTEM PROMPT
    prompt = f"""
    You are the specialized AI Engine for {BUSINESS_NAME}. 
    Analyze this salvage image and perform the following:

    1. IDENTIFICATION: Identify the most prominent industrial salvage object.
    2. CLASSIFICATION: Map it against the 120-file industrial schema.
    3. SKU GENERATION: Create a machine-readable SKU based on attributes (e.g., BRAND-TYPE-COND).
    4. NLP SALES COPY: Use Neurolinguistic Programming techniques:
       - Use 'Pattern Interruption' in the headline.
       - Use 'Embedded Commands' (e.g., "Imagine the reliability this brings...") in the body.
       - Provide two versions: FB Marketplace (casual/trust) and Radwell (technical/spec-heavy).

    Return valid JSON ONLY:
    {{
      "object_name": "string",
      "sku": "string",
      "drive_doc_id": "{file_name}",
      "listings": {{
        "facebook": "string",
        "radwell": "string"
      }}
    }}
    """

    response = model.generate_content(
        [Image.from_bytes(image_bytes), prompt],
        generation_config={"response_mime_type": "application/json"}
    )
    
    analysis_result = json.loads(response.text)

    # 4. Store the results in Cloud SQL
    try:
        conn = psycopg2.connect(
            host=os.environ.get("DB_HOST"), # Injected by Terraform /cloudsql/...
            database=os.environ.get("DB_NAME"),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASS")
        )
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO inventory (sku, doc_id, data) VALUES (%s, %s, %s)",
            (analysis_result['sku'], file_name, json.dumps(analysis_result))
        )
        conn.commit()
        cur.close()
        conn.close()
        print(f"Successfully cataloged SKU: {analysis_result['sku']}")
    except Exception as e:
        print(f"Database error: {e}")

    # Cleanup /tmp to save memory
    os.remove(raw_path)
    os.remove(processed_path)

    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
