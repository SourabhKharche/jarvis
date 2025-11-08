from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
client = OpenAI(api_key=OPENAI_API_KEY)

@app.route('/')
def home():
    return "Jarvis AI backend is running!"

@app.route('/ai-process', methods=['POST'])
def ai_process():
    data = request.json
    command = data.get("command")

    # Ask OpenAI to interpret the command
    prompt = f"""
    You are an AI assistant that turns user commands into JSON.
    Example:
    Input: "Remind me to call mom at 8 PM"
    Output: {{
        "action": "reminder",
        "time": "20:00",
        "message": "call mom"
    }}

    Now interpret this:
    "{command}"
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    ai_output = response.choices[0].message.content
    return jsonify({"ai_output": ai_output})

if __name__ == '__main__':
    app.run(debug=True)
