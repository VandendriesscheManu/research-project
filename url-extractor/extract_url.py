#!/usr/bin/env python3
"""
Extracts the trycloudflare.com URL from cloudflared container logs
and persists it to a .env file for the frontend to use.
"""
import os
import re
import time
import subprocess
from pathlib import Path

CONTAINER_NAME = "cloudflared"
ENV_FILE = "/shared/.env.public"
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

def write_to_env_file(url):
    """
    Write the PUBLIC_API_BASE_URL to the shared env file.
    """
    try:
        env_path = Path(ENV_FILE)
        env_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write the URL
        with open(ENV_FILE, 'w') as f:
            f.write(f"PUBLIC_API_BASE_URL={url}\n")
        
        print(f"✅ Written to {ENV_FILE}")
        return True
    except Exception as e:
        print(f"❌ Failed to write to env file: {e}")
        return False

def main():
    print("🚀 Starting Cloudflare URL extractor...")
    print(f"📦 Monitoring container: {CONTAINER_NAME}")
    print(f"📝 Target env file: {ENV_FILE}")
    print()
    
    # Extract URL from logs
    url = extract_url_from_logs()
    
    if not url:
        print(f"❌ Failed to extract URL after {MAX_RETRIES} attempts")
        exit(1)
    
    # Write to env file
    if write_to_env_file(url):
        print()
        print("=" * 60)
        print("✅ SUCCESS! Cloudflare URL is ready:")
        print(f"   {url}")
        print("=" * 60)
        print()
        print("The frontend can now access this URL from the env file.")
        
        # Keep the container running so Docker knows it succeeded
        # In a real scenario, you might want to run a health check server
        print("📌 Keeping container alive...")
        while True:
            time.sleep(3600)  # Sleep for 1 hour
    else:
        exit(1)

if __name__ == "__main__":
    main()
