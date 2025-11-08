import os
import openai

def interpret_command(text):
    # Load your OpenAI key from environment variable
    openai.api_key = os.getenv("OpenAI_API_key")
    if not openai.api_key:
        raise ValueError("Missing OPENAI_API_KEY environment variable")

    client = openai.OpenAI()

    # Send the text to GPT and get a structured command as response
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content":
             "You are a helpful personal assistant. Respond in a short, single block of JSON. "
             "If the user says 'note this down', extract the note as {action:'note','content':'...'}; "
             "if they ask 'what did I ask you to note?', reply with {action:'retrieve'}; "
             "otherwise reply as {action:'info', 'content':'...'}."
            },
            {"role": "user", "content": text}
        ],
    )

    # Parse and return the response text (which should be a JSON string)
    return response.choices[0].message.content
