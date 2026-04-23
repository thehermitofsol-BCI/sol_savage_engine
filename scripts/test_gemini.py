# File: scripts/test_gemini.py
import os
import requests
import json

api_key = os.getenv("AIzaSyCET5MQ38Om2be44ZUghmC-VUtRy7PInXI")

# 2026 PRODUCTION UPGRADE
MODEL_ID = "gemini-3-flash-preview"
url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_ID}:generateContent?key={api_key}"

payload = {
    "contents": [{"parts": [{"text": "CTO Handshake: Protocol 2026. Status check?"}]}]
}

print(f"[*] Connecting to Gemini 3 Node...")
try:
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        print("[✓] HANDSHAKE SUCCESSFUL.")
        data = response.json()
        print(f"Response: {data['candidates'][0]['content']['parts'][0]['text']}")
    else:
        print(f"[X] HANDSHAKE FAILED: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"[X] ERROR: {str(e)}")
