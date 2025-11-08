import openai

def interpret_command(text, api_key):
    openai.api_key = api_key
    prompt = (
        "You are a personal assistant. Respond with JSON. "
        "If the user says 'note this down', extract the note, "
        "if user asks 'what did I ask you to note?', reply 'retrieve', "
        "otherwise classify as info."
    )
    response = openai.ChatCompletion.create(
        model="gpt-4o",  # Or your chosen model
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content  # Return GPT JSON string
