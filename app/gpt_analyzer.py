import openai, os
openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_failures(failure):
    prompt = f"""Test: {failure['name']}
Error: {failure['message']}
Trace: {failure['trace']}
Explain cause:"""
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return {"test": failure["name"], "reason": response.choices[0].message["content"]}
