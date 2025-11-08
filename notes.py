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

    save_to_firestore(user_id, "notes", {"content": content})
    return jsonify({"status": "✅ Note saved", "content": content})
