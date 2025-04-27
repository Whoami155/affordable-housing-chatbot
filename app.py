from flask import Flask, request, jsonify, render_template
import requests
import traceback

app = Flask(__name__, static_folder="static", template_folder="templates")

# Make sure this is a valid, active OpenRouter API key
OPENROUTER_API_KEY = "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"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "").strip()
    if not user_input:
        return jsonify({"response": "Please enter a valid message."})

    show_model = any(word in user_input.lower() for word in ["3d", "model", "architecture", "glb", "render"])
    if show_model:
        return jsonify({
            "response": "Here is a 3D architectural model for you to explore 👇",
            "show_model": True
        })

    data = {
        "model": "anthropic/claude-3-sonnet",
        "messages": [{"role": "user", "content": user_input}],
        "max_tokens": 300
    }

    res = None
    try:
        res = requests.post(API_URL, headers=HEADERS, json=data)
        print("[STATUS CODE]", res.status_code)
        print("[RESPONSE TEXT]", res.text)
        res.raise_for_status()

        json_response = res.json()
        print("[FULL JSON]", json_response)

        reply = json_response["choices"][0]["message"]["content"]
        return jsonify({"response": reply, "show_model": False})

    except Exception as e:
        print("[ERROR]", str(e))
        traceback.print_exc()
        if res is not None:
            print("[RAW RESPONSE]", res.text)
        return jsonify({"response": "Sorry, an error occurred while fetching the response."})


if __name__ == "__main__":
    app.run(debug=True)

