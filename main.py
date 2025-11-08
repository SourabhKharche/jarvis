import firebase_utils
import gpt_handler
import elevenlabs_utils   # Optional

# Setup
OPENAI_API_KEY = "your-openai-key"
ELEVEN_API_KEY = "your-elevenlabs-key"
USER_ID = "user1"

db = firebase_utils.init_firebase()

# Example function: handle user input
def handle_input(text):
    intent_json = gpt_handler.interpret_command(text, OPENAI_API_KEY)
    # Parse intent_json here. For demo, let's assume intent_json = '{"action":"note","content":"Buy milk"}'

    import json
    intent = json.loads(intent_json)
    action = intent.get("action")
    content = intent.get("content")

    if action == "note":
        firebase_utils.save_note(db, USER_ID, content)
        reply = "Got it, I noted: " + content
    elif action == "retrieve":
        notes = firebase_utils.get_notes(db, USER_ID)
        if notes:
            reply = "You asked me to note: " + ", ".join(n['text'] for n in notes)
        else:
            reply = "No notes recorded."
    else:
        reply = content   # Info result or GPT reply

    # Optionally: convert to speech
    # elevenlabs_utils.text_to_speech(reply, ELEVEN_API_KEY)

    return reply

# Example usage
if __name__ == "__main__":
    text = input("Enter your command: ")
    print(handle_input(text))
