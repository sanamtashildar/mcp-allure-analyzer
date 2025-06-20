import openai
import os

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_failures(failure):
    prompt = f"""Why did the following test fail?

Test: {failure['name']}
Error: {failure['message']}
Give a short explanation."""

    print(f"Sending prompt to OpenAI: {prompt}")  # Log the prompt

    response = client.chat.completions.create(
        model="gpt-4o",  # or gpt-3.5-turbo
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100
    )

    reason = response.choices[0].message.content
    print(f"Received reason from OpenAI: {reason}")  # Log the response

    return {"test": failure["name"], "reason": reason}
