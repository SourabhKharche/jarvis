import firebase_utils
import gpt_handler
import json

USER_ID = "user1"

def handle_input(text):
    # Send text to GPT for command interpretation
    intent_json = gpt_handler.interpret_command(text)

    print("GPT responded:", intent_json)  # For debug

    # Parse intent from the JSON string
    try:
        intent = json.loads(intent_json)
    except Exception as e:
        return f"Sorry, couldn't parse intent: {e}"

    action = intent.get('action')
    content = intent.get('content')

    # Initialize Firebase (once, outside the function is best)
    db = firebase_utils.init_firebase()

    if action == "note" and content:
        firebase_utils.save_note(db, USER_ID, content)
        return f"Got it, I noted: {content}"

    elif action == "retrieve":
        notes = firebase_utils.get_notes(db, USER_ID)
        if notes:
            return f"Your notes: " + ", ".join(n['text'] for n in notes)
        else:
            return "No notes recorded."

    elif action == "info" and content:
        return content

    else:
        return "Sorry, I didn't understand the command."

if __name__ == "__main__":
    while True:
        text = input("Enter your command (or 'quit' to exit): ")
        if text.strip().lower() == "quit":
            break
        reply = handle_input(text)
        print(reply)
