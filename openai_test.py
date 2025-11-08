import os
import openai

def main():
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("Missing OPENAI_API_KEY environment variable")

    # Use the new 'client' and 'chat.completions.create' interface
    client = openai.OpenAI()

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say hello in a friendly way."}
        ],
    )

    print("GPT Response:", response.choices[0].message.content)

if __name__ == "__main__":
    main()
