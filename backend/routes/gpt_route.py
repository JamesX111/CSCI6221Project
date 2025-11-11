from flask import Blueprint, request, jsonify
from datetime import datetime
from openai import OpenAI
import json


bp = Blueprint('gpt', __name__, url_prefix='/api/gpt')

with open("config/gpt_config.json", "r") as f:
    gpt_config = json.load(f)
api_key = gpt_config.get("OPENAI_API_KEY")
model = gpt_config.get("MODEL", "gpt-3.5-turbo")
system_prompt = gpt_config.get("SYSTEM_PROMPT", "You are a helpful assistant.")

@bp.route("/chat", methods=["POST"])
def chat():
    """
    Chat endpoint for GPT service.

    Expected JSON body:
    {
        "user_message": "Hello!",
        "chat_history": [
            {"role": "user", "content": "Hi"},
            {"role": "assistant", "content": "Hello! How can I help?"}
        ]
    }
    """

    data = request.get_json()

    if not data or "user_message" not in data:
        return jsonify({"error": "Missing user_message"}), 400

    user_message = data["user_message"]
    chat_history = data.get("chat_history", [])

    

    # Initialize OpenAI client (on demand)
    client = OpenAI(api_key=api_key)

    messages = [{"role": "system", "content": system_prompt}]
    messages += chat_history
    messages.append({"role": "user", "content": user_message})

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages
        )
        reply = response.choices[0].message.content
        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500