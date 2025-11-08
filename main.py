import notes
import reminders
#import info
import gpt_handler
import firebase_utils
import json

USER_ID = "user1"

# Initialize Firebase once at startup
db = firebase_utils.init_firebase()

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
    time = intent.get('time', None)

    # Route commands to the correct module
    if action in ["note", "take note", "note this down","create a note"] and content:
        # Save a note and acknowledge
        return notes.take_note(db, USER_ID, content)

    elif action in ["get notes","what did i ask you to note","retrieve notes","what was the note","what was in the note"]:
        # Retrieve notes for this user
        return notes.get_notes(db, USER_ID)

    elif action in ["set reminder","remember","remind me"] and content:
        # Set a reminder; if time is None, handle default logic inside reminders.py
        return reminders.set_reminder(db, USER_ID, content, time)

    elif action in ["get reminders","what did i ask you to remember","what was the reminder"]:
        # Get all reminders for this user
        return reminders.get_reminders(db, USER_ID)

    #elif action == "info" and content:
        # Get general info (using GPT or API logic inside info.py)
        #return info.get_general_info(content)

    else:
        return "Sorry, I didn't understand the command."

if __name__ == "__main__":
    while True:
        text = input("Enter your command (or 'quit' to exit): ")
        if text.strip().lower() == "quit":
            break
        reply = handle_input(text)
        print(reply)
