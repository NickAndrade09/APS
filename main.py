import os
import requests
from flask import Flask, request, render_template, jsonify
from dotenv import load_dotenv
import openai

load_dotenv()

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

JOOBLE_API_URL = "https://jooble.org/api/"
JOOBLE_API_KEY = os.getenv("JOOBLE_API_KEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")

    prompt = f"""
    Você é um assistente de carreira. O usuário digitou: "{user_input}".
    Baseado nisso, pergunte mais sobre a experiência dele ou sugira vagas de emprego.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    reply = response["choices"][0]["message"]["content"]
    return jsonify({"response": reply})

@app.route("/jobs", methods=["POST"])
def jobs():
    keywords = request.json.get("keywords")
    location = request.json.get("location")

    payload = {
        "keywords": keywords,
        "location": location
    }

    res = requests.post(f"{JOOBLE_API_URL}{JOOBLE_API_KEY}", json=payload)
    jobs = res.json().get("jobs", [])[:5]  # Retorna as 5 primeiras

    return jsonify(jobs)

if __name__ == "__main__":
    app.run(debug=True)
