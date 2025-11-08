from flask import Blueprint, request, jsonify
import firebase_utils  # Import firebase_utils for CLI/helper use

notes_bp = Blueprint("notes_bp", __name__)

@notes_bp.route("/note", methods=["POST"])
def handle_note():
    data = request.json or {}
    content = data.get("content")
    user_id = data.get("user_id", "user1")

    if not content:
        return jsonify({"error": "Missing note content"}), 400

    firebase_utils.save_note(user_id, content)
    return jsonify({"status": "✅ Note saved", "content": content})

# CLI/assistant-compatible wrapper
def save_note(db, user_id, note_text):
    firebase_utils.save_note(user_id, note_text)
    return f"Saved note: {note_text}"

def get_notes(db, user_id):
    notes_list = firebase_utils.get_notes(user_id)
    if not notes_list:
        return "No notes found."
    return "Your notes:\n" + "\n".join(n['text'] for n in notes_list)
