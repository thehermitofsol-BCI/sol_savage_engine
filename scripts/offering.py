# Operations Node: offering.py
# Logic for delivering the Genesis Offering.
# Version: 8.2.4 - Key Sync

import os
import json
import requests

# Ensure this URL matches your LATEST 'New Deployment' URL
URL = "https://script.google.com/macros/s/AKfycbxxeVDngdvjCJv8VXlob12WoQY8qD60TRkoXe1fiCmd2ZlESIkxZ2fVG7apOce4mEAE/exec"

def deliver():
    target = "constitution.md"
    
    if not os.path.exists(target):
        print(f"Error: {target} not found in current directory.")
        return
    
    # Verify local file is not empty before sending
    file_size = os.path.getsize(target)
    if file_size == 0:
        print(f"Error: {target} is 0 bytes locally. Aborting.")
        return
    
    with open(target, "r") as f:
        file_content = f.read()
        
    # Payload keys: fileName, content, and message
    payload = {
        "fileName": "constitution.md",
        "content": file_content,
        "message": "Sol Savage Genesis: v8.2.4 Sync"
    }
    
    print(f"Initiating delivery of {target} ({file_size} bytes)...")
    
    try:
        response = requests.post(
            URL, 
            data=json.dumps(payload), 
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Network Status: {response.status_code}")
        print(f"Handshake Result: {response.text}")
        
    except Exception as e:
        print(f"Connection Failure: {e}")

if __name__ == "__main__":
    deliver()
7
