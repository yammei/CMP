import subprocess

# Checks server status by curl-ing the API's test endpoint.
def check_test_endpoint_status() -> None:
    try:
        test_url: str = "http://127.0.0.1:5000/api/test"
        command: str = f"curl -X GET {test_url}"
        response = subprocess.run(command, shell=True)
        print(f"[SUCCESS] Ran test command: {command}")
    except Exception as e:
        print(f"[ERROR]: {e}")