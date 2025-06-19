
def analyze_failures(failure):
    return {
        "test": failure["name"],
        "reason": f"Mocked GPT analysis for: {failure['message']}"
    }
