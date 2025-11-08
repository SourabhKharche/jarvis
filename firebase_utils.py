import firebase_admin
from firebase_admin import credentials, firestore
import datetime

def save_reminder(db, userid, message, reminder_time=None):

    reminders_ref = db.collection("users").document(userid).collection("reminders")
    reminder_data = {
        "message": message,
        "created_at": datetime.datetime.utcnow(),
    }
    if reminder_time:
        reminder_data["reminder_time"] = reminder_time
    reminders_ref.add(reminder_data)
    return f"Reminder saved: \"{message}\"" + (f" at {reminder_time}" if reminder_time else "")

def get_reminder(db, userid, content, time):

    reminders_ref = db.collection("users").document(userid).collection("reminders")
    reminders = reminders_ref.order_by("created_at", direction=firestore.Query.DESCENDING).stream()
    current_time = datetime.datetime.utcnow()
    due = []
    latest = None

    for doc in reminders:
        r = doc.to_dict()
        if not latest:
            latest = r
        if "reminder_time" in r:
            try:
                rt = datetime.datetime.fromisoformat(r["reminder_time"])
                if rt <= current_time:
                    due.append(r)
            except Exception:
                pass

    if due:
        return "Reminders due:\n" + "\n".join([f"- {r['message']} (for {r['reminder_time']})" for r in due])
    elif latest:
        return f"Latest reminder: {latest['message']}" + (f" (for {latest.get('reminder_time')})" if "reminder_time" in latest else "")
    else:
        return "No reminders found."


def init_firebase():
    cred = credentials.Certificate('serviceAccountKey.json')
    firebase_admin.initialize_app(cred)
    return firestore.client()

def save_note(db, user_id, note_text):
    notes_ref = db.collection('users').document(user_id).collection('notes')
    notes_ref.add({
        'text': note_text,
        'timestamp': datetime.datetime.utcnow()
    })

def get_notes(db, user_id):
    notes_ref = db.collection('users').document(user_id).collection('notes')
    notes = notes_ref.order_by('timestamp').stream()
    return [note.to_dict() for note in notes]
