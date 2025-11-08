from flask import Blueprint, request, jsonify
from firebase_utils import save_note, get_notes

notes_bp = Blueprint("notes_bp", __name__)

@notes_bp.route("/note", methods=["POST"])
def handle_note():
    data = request.json or {}
    content = data.get("content")
    user_id = data.get("user_id", "user1")

    if not content:
        return jsonify({"error": "Missing note content"}), 400

    save_note(user_id, content)
    return jsonify({"status": "✅ Note saved", "content": content})

# CLI/assistant-compatible wrapper
def save_note(db, user_id, note_text):
    save_note(user_id, note_text)
    return f"Saved note: {note_text}"

def get_notes(db, user_id):
    notes_list = get_notes(user_id)
    if not notes_list:
        return "No notes found."
    return "Your notes:\n" + "\n".join(n['text'] for n in notes_list)
