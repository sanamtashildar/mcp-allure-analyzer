import os, json

def parse_allure_results(results_dir):
    failures = []
    for root, _, files in os.walk(results_dir):
        for file in files:
            if file.endswith("-result.json"):
                with open(os.path.join(root, file)) as f:
                    data = json.load(f)
                    if data.get("status") == "failed":
                        failures.append({
                            "name": data.get("name"),
                            "message": data.get("statusDetails", {}).get("message", ""),
                            "trace": data.get("statusDetails", {}).get("trace", "")
                        })
    return failures
