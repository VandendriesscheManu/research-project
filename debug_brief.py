"""
Debug script to check brief_id for a session_id
"""
import requests
import sys

API_KEY = "demo-123"
API_BASE = "http://localhost:8001"

if len(sys.argv) < 2:
    print("Usage: python debug_brief.py <session_id>")
    sys.exit(1)

session_id = sys.argv[1]

headers = {"X-API-KEY": API_KEY}

try:
    # Get the brief
    response = requests.get(
        f"{API_BASE}/product-brief/{session_id}",
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Brief found!")
        print(f"   Brief ID: {data.get('brief_id') or data.get('id')}")
        print(f"   Session ID: {data.get('session_id')}")
        print(f"   Product Name: {data.get('product_name')}")
        print(f"   Created: {data.get('created_at')}")
    elif response.status_code == 404:
        print(f"❌ No brief found for session: {session_id}")
    else:
        print(f"❌ Error {response.status_code}: {response.text}")
        
except Exception as e:
    print(f"❌ Error: {e}")
