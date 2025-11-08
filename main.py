import notes
import reminders
#import info
import gpt_handler
import firebase_utils
import json
import re

def clean_gpt_json(text):
    # Remove markdown code block (e.g., ``````)
    # Handles with/without "json" and line breaks
    return re.sub(r"^``````$", "", text.strip(), flags=re.IGNORECASE)


USER_ID = "user1"

# Initialize Firebase once at startup
db = firebase_utils.init_firebase()

def action_matches(action, *options):
    return action and action.lower() in [opt.lower() for opt in options]

def clean_gpt_json(text):
    # Remove markdown code block if present (e.g., `````` or ``````)
    return re.sub(r"^``````$", "", text.strip(), flags=re.IGNORECASE | re.MULTILINE)

def handle_input(text):
    # Send text to GPT for command interpretation
    intent_json = gpt_handler.interpret_command(text)
    print("GPT responded:", intent_json)  # For debug

    # Clean up formatting from GPT's response (if any)
    intent_json_clean = clean_gpt_json(intent_json)

    # Parse intent from the JSON string
   intent_json_clean = clean_gpt_json(intent_json)
    try:
        intent = json.loads(intent_json_clean)
    except Exception as e:
        return f"Sorry, couldn't parse intent: {e}"


    action = intent.get('action')
    content = intent.get('content')
    time = intent.get('time', None)

    # Route commands to the correct module (case-insensitive, supports many synonyms)
    if action_matches(action, "note", "take note", "note this down", "create a note", "note_create", "add_note"):
        return notes.save_note(db, USER_ID, content)

    elif action_matches(action, "get notes", "what did i ask you to note", "retrieve notes", "what was the note", "what was in the note", "note_retrieve", "notes_retrieve", "get_notes"):
        return notes.get_notes(db, USER_ID)

    elif action_matches(action, "set reminder", "remember", "remind me", "reminder_create", "save_reminder") and content:
        return reminders.set_reminder(db, USER_ID, content, time)

    elif action_matches(action, "get reminders", "what did i ask you to remember", "what was the reminder", "reminders_retrieve", "get_reminders"):
        return reminders.get_reminders(db, USER_ID)

    #elif action_matches(action, "info", "get info", "info_query") and content:
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
