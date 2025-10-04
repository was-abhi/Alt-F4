from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import requests

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Gemini API key from https://aistudio.google.com/api-keys
API_KEY = os.getenv("API_KEY")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message")

    if not API_KEY:
        return jsonify({"reply": "API_KEY not found. Please set it in your .env file."}), 500

    try:
        # Gemini (Google AI Studio) endpoint
        response = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}",
            headers={
                "Content-Type": "application/json"
            },
            json={
                "contents": [
                    {
                        "role": "user",
                        "parts": [
                            {"text": user_msg}
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.7,
                    "topP": 0.9,
                    "topK": 40,
                    "maxOutputTokens": 300
                },
                "safetySettings": [
                    {"category": "HARM_CATEGORY_DEROGATORY", "threshold": "BLOCK_ONLY_HIGH"},
                    {"category": "HARM_CATEGORY_VIOLENCE", "threshold": "BLOCK_ONLY_HIGH"},
                    {"category": "HARM_CATEGORY_SEXUAL", "threshold": "BLOCK_ONLY_HIGH"},
                    {"category": "HARM_CATEGORY_DANGEROUS", "threshold": "BLOCK_ONLY_HIGH"}
                ]
            }
        )

        data = response.json()

        # Check for block reasons or errors from Gemini
        if "candidates" not in data or not data["candidates"]:
            if "promptFeedback" in data and "blockReason" in data["promptFeedback"]:
                return jsonify({"reply": f"Your prompt was blocked by Gemini: {data['promptFeedback']['blockReason']}"})
            return jsonify({"reply": "MovBot could not generate a response."})

        # Gemini responses are nested deeper
        reply = data["candidates"][0]["content"]["parts"][0]["text"]

        return jsonify({"reply": reply})

    except requests.exceptions.RequestException as e:
        print(f"Network or API request error: {e}")
        return jsonify({"reply": "MovBot is having trouble connecting. Please try again later."}), 500
    except Exception as e:
        print("API error:", e)
        return jsonify({"reply": "Oops, something went wrong with MovBot."}), 500

if __name__ == "__main__":
    app.run(debug=True)
