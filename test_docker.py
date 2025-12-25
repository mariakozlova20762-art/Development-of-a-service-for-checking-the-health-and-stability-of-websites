# test_docker.py
import requests
import time
import sys

def test_docker_container():
    max_retries = 10
    retry_delay = 2
    
    print("Testing Docker container...")
    
    for i in range(max_retries):
        try:
            response = requests.get("http://localhost:8000/api/v1/health", timeout=5)
            if response.status_code == 200:
                print("✅ Container is running and healthy!")
                
                # Test API endpoints
                print("\nTesting API endpoints:")
                
                # Test single website
                response = requests.get("http://localhost:8000/api/v1/check/example.com")
                print(f"Single check: {response.status_code}")
                
                # Test multiple websites
                response = requests.post(
                    "http://localhost:8000/api/v1/check/multiple",
                    json=["example.com", "google.com"]
                )
                print(f"Multiple check: {response.status_code}")
                
                return True
        except requests.exceptions.ConnectionError:
            print(f"⏳ Waiting for container... ({i+1}/{max_retries})")
            time.sleep(retry_delay)
    
    print("❌ Container failed to start")
    return False

if __name__ == "__main__":
    success = test_docker_container()

    sys.exit(0 if success else 1)
