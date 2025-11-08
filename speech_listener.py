import time
import firebase_utils
from main import handle_input  # Make sure main.py is importable and not only __main__
from google.cloud import firestore

USER_ID = "user1"  # Modify as needed
COLLECTION_NAME = "speech_to_text"  # The Firestore subcollection for transcripts
PROCESS_FIELD = "processed"         # Field for marking handled transcripts
CHECK_INTERVAL = 5                 # Seconds between polls

def poll_speech_to_text():
    db = firebase_utils.init_firebase()
    # Path: users/{USER_ID}/speech_to_text
    speech_collection = db.collection("users").document(USER_ID).collection(COLLECTION_NAME)

    while True:
        print(f"Polling {COLLECTION_NAME} for unprocessed items...")
        docs = speech_collection.where(PROCESS_FIELD, "==", False).stream()

        for doc in docs:
            data = doc.to_dict()
            speech_text = data.get("text")
            if not speech_text:
                continue

            print(f"Found speech-to-text input: {speech_text}")
            result = handle_input(speech_text)  # Directly feed to Jarvis
            print(f"Jarvis Output:\n{result}")

            # Mark as processed so Jarvis doesn't repeat it
            speech_collection.document(doc.id).update({PROCESS_FIELD: True})

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    poll_speech_to_text()
