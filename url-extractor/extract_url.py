#!/usr/bin/env python3
"""
Extracts the trycloudflare.com URL from cloudflared container logs
and persists it to a GitHub Gist for the frontend to use.
"""
import os
import re
import time
import subprocess
import requests

CONTAINER_NAME = "cloudflared"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # Your GitHub Personal Access Token
GIST_ID = os.getenv("GIST_ID")  # Your existing Gist ID (or leave empty to create new)
MAX_RETRIES = 60  # Wait up to 60 seconds
RETRY_INTERVAL = 1  # Check every second

def extract_url_from_logs():
    """
    Continuously monitor cloudflared logs until URL appears.
    Returns the extracted URL or None if not found.
    """
    url_pattern = re.compile(r'https://[a-z0-9-]+\.trycloudflare\.com')
    
    for attempt in range(MAX_RETRIES):
        try:
            # Get logs from the cloudflared container
            result = subprocess.run(
                ["docker", "logs", CONTAINER_NAME],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            logs = result.stdout + result.stderr
            match = url_pattern.search(logs)
            
            if match:
                url = match.group(0)
                print(f"✅ Found Cloudflare URL: {url}")
                return url
            
            print(f"⏳ Waiting for URL... (attempt {attempt + 1}/{MAX_RETRIES})")
            time.sleep(RETRY_INTERVAL)
            
        except subprocess.TimeoutExpired:
            print(f"⚠️ Docker logs command timed out (attempt {attempt + 1})")
            time.sleep(RETRY_INTERVAL)
        except Exception as e:
            print(f"⚠️ Error reading logs: {e}")
            time.sleep(RETRY_INTERVAL)
    
    return None

def update_gist(url):
    """
    Update or create a GitHub Gist with the Cloudflare URL.
    """
    if not GITHUB_TOKEN:
        print("❌ GITHUB_TOKEN not set in environment variables")
        return False
    
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    gist_content = {
        "description": "Cloudflare Tunnel URL for Marketing Plan Generator",
        "public": False,
        "files": {
            "cloudflare_url.txt": {
                "content": url
            }
        }
    }
    
    try:
        if GIST_ID:
            # Update existing Gist
            response = requests.patch(
                f"https://api.github.com/gists/{GIST_ID}",
                headers=headers,
                json=gist_content
            )
            if response.status_code == 200:
                print(f"✅ Updated existing Gist: {GIST_ID}")
                print(f"📎 Raw URL: {response.json()['files']['cloudflare_url.txt']['raw_url']}")
                return True
            else:
                print(f"❌ Failed to update Gist: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
        else:
            # Create new Gist
            response = requests.post(
                "https://api.github.com/gists",
                headers=headers,
                json=gist_content
            )
            if response.status_code == 201:
                gist_data = response.json()
                new_gist_id = gist_data['id']
                raw_url = gist_data['files']['cloudflare_url.txt']['raw_url']
                print(f"✅ Created new Gist!")
                print(f"📋 Gist ID: {new_gist_id}")
                print(f"📎 Raw URL: {raw_url}")
                print()
                print("⚠️  IMPORTANT: Add these to your .env file:")
                print(f"   GIST_ID={new_gist_id}")
                print(f"   GIST_RAW_URL={raw_url}")
                return True
            else:
                print(f"❌ Failed to create Gist: {response.status_code}")
                print(f"   Response: {response.text}")
                return False
    except Exception as e:
        print(f"❌ Error updating Gist: {e}")
        return False

def write_to_env_file(url):
    """
    DEPRECATED: Kept for backward compatibility.
    Now using GitHub Gist instead of local file.
    """
    print("⚠️  write_to_env_file is deprecated. Using GitHub Gist instead.")
    return True

def main():
    print("🚀 Starting Cloudflare URL extractor...")
    print(f"📦 Monitoring container: {CONTAINER_NAME}")
    print(f"🌐 Publishing to: GitHub Gist")
    print()
    
    # Extract URL from logs
    url = extract_url_from_logs()
    
    if not url:
        print(f"❌ Failed to extract URL after {MAX_RETRIES} attempts")
        exit(1)
    
    # Update GitHub Gist
    if update_gist(url):
        print()
        print("=" * 60)
        print("✅ SUCCESS! Cloudflare URL is published to GitHub Gist:")
        print(f"   {url}")
        print("=" * 60)
        print()
        print("The frontend can now access this URL from the Gist.")
        
        # Keep the container running so Docker knows it succeeded
        print("📌 Keeping container alive...")
        while True:
            time.sleep(3600)  # Sleep for 1 hour
    else:
        print("❌ Failed to publish URL to GitHub Gist")
        exit(1)
        exit(1)

if __name__ == "__main__":
    main()
