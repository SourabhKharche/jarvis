from flask import Blueprint, request, jsonify
from firebase_utils import save_to_firestore

reminders_bp = Blueprint("reminders_bp", __name__)

@reminders_bp.route("/reminder", methods=["POST"])
def handle_reminder():
    data = request.json or {}
    message = data.get("message")
    time = data.get("time")
    user_id = data.get("user_id", "user1")

    if not message:
        return jsonify({"error": "Missing reminder message"}), 400

    reminder = {"message": message, "time": time or "unspecified"}
    save_to_firestore(user_id, "reminders", reminder)
    return jsonify({"status": "✅ Reminder saved", "data": reminder})
