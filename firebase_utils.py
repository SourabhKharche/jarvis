import firebase_admin
from firebase_admin import credentials, firestore
import datetime

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
