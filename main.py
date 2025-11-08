import notes
import reminders
# import info
import gpt_handler
import firebase_utils
import json
import re

def clean_gpt_json(text: str) -> str:
    """
    Removes triple-backtick code blocks (with or without language tags like 'json').
    Handles both single-object and array JSON in responses.
    """
    # Match opening code fence (with or without "json"), then the rest, then closing code fence
    # Greedy enough for multi-line JSON array responses
    cleaned = re.sub(r'^``````$', '', text.strip(), flags=re.IGNORECASE)
    return cleaned

USER_ID = "user1"

# Initialize Firebase once at startup
db = firebase_utils.init_firebase()

def action_matches(action, *options):
    return action and action.lower() in [opt.lower() for opt in options]

def handle_input(text):
    # Send text to GPT for command interpretation
    intent_json = gpt_handler.interpret_command(text)
    print("GPT responded:", intent_json)  # For debug

    intent_json_clean = clean_gpt_json(intent_json)
    print("Cleaned GPT JSON:", intent_json_clean)  # For debug

    try:
        # Accept both a list (multiple actions) or a single object
        parsed = json.loads(intent_json_clean)
        intents = parsed if isinstance(parsed, list) else [parsed]
    except Exception as e:
        return f"Sorry, couldn't parse intent: {e}"

    results = []
    for intent in intents:
        action = intent.get('action')
        content = intent.get('content')
        time = intent.get('time', None)

        # Route commands to the correct module (case-insensitive, supports many synonyms)
        if action_matches(action, "note", "take note", "note this down", "create a note", "note_create", "add_note"):
            results.append(notes.save_note(db, USER_ID, content))

        elif action_matches(action, "get notes", "what did i ask you to note", "retrieve notes", "what was the note", "what was in the note", "note_retrieve", "notes_retrieve", "get_notes"):
            results.append(notes.get_notes(db, USER_ID))

        elif action_matches(action, "set reminder", "remember", "remind me", "reminder_create", "save_reminder"):
            results.append(reminders.set_reminder(db, USER_ID, content, time))

        elif action_matches(action, "get reminders", "what did i ask you to remember", "what was the reminder", "reminders_retrieve", "get_reminders"):
            results.append(reminders.get_reminders(db, USER_ID))

        # elif action_matches(action, "info", "get info", "info_query") and content:
        #     results.append(info.get_general_info(content))

        else:
            results.append("Sorry, I didn't understand the command.")

    return "\n".join(results)

if __name__ == "__main__":
    while True:
        text = input("Enter your command (or 'quit' to exit): ")
        if text.strip().lower() == "quit":
            break
        reply = handle_input(text)
        print(reply)
