import json
import os

def parse_allure_results(folder_path):
    failures = []
    for file in os.listdir(folder_path):
        if file.endswith("-result.json"):
            with open(os.path.join(folder_path, file)) as f:
                data = json.load(f)
                if data.get("status") in ["failed", "broken"]:
                    failures.append({
                        "name": data.get("name"),
                        "message": data.get("statusDetails", {}).get("message", "No message")
                    })
    return failures
