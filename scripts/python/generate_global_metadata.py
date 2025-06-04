# scripts/python/generate_global_metadata.py
import uuid
import json
import sys

def main():
    deployment_id = str(uuid.uuid4())  
    result = {"deployment_id": deployment_id}
    json.dump(result, sys.stdout)  

if __name__ == "__main__":
    main()