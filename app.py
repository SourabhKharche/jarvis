from flask import Flask, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI
import firebase_admin
from firebase_admin import credentials, firestore
import os

# Load .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
FIREBASE_CREDENTIALS = os.getenv("FIREBASE_CREDENTIALS")
MODEL = os.getenv("MODEL", "gpt-4o-mini")

# Init Firebase
cred = credentials.Certificate(FIREBASE_CREDENTIALS)
firebase_admin.initialize_app(cred)
db = firestore.client()

# Init OpenAI client (new SDK format)
client = OpenAI(api_key=OPENAI_API_KEY)

# Flask App
app = Flask(__name__)

# Import route blueprints
from routes.notes import notes_bp
from routes.reminders import reminders_bp

# Register blueprints
app.register_blueprint(notes_bp)
app.register_blueprint(reminders_bp)

@app.route("/")
def home():
    return "✅ Jarvis backend is running with real GPT + Firebase"

@app.route("/ai-process", methods=["POST"])
def ai_process():
    data = request.json or {}
    command = data.get("command")
    user_id = data.get("user_id", "user1")

    if not command:
        return jsonify({"error": "missing 'command'"}), 400

    prompt = f"""
    You are a JSON-only assistant. Convert commands into structured JSON.

    Examples:
    "Make a note that I need to buy milk" ->
    {{"action": "note", "content": "I need to buy milk"}}

    "Remind me to call mom at 6 PM" ->
    {{"action": "reminder", "message": "call mom", "time": "18:00"}}

    Now convert this:
    "{command}"
    """

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.choices[0].message.content
    print("🔍 GPT OUTPUT:", raw)

    try:
        parsed = eval(raw)  # Converts string JSON into Python dict
    except:
        return jsonify({"error": "GPT returned invalid JSON", "raw": raw})

    # Route dynamically
    if parsed.get("action") == "note":
        return forward_to("notes_bp.handle_note", {"content": parsed["content"], "user_id": user_id})
    elif parsed.get("action") == "reminder":
        return forward_to("reminders_bp.handle_reminder", {"message": parsed["message"], "time": parsed.get("time"), "user_id": user_id})
    else:
        return jsonify({"error": "unknown action", "parsed": parsed})

def forward_to(handler_name, json_data):
    """Helper to forward parsed data into the correct route function"""
    with app.test_request_context(json=json_data):
        return app.view_functions[handler_name]()

if __name__ == "__main__":
    app.run(debug=True)
