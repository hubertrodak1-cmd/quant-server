import os
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")


@app.route("/analizuj", methods=["POST"])
def analizuj():
  dane = request.json
  aktywo = dane.get("aktywo", "BTC-USD")
  aktualna_cena = dane.get("cena", 0.0)

  headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {GROQ_API_KEY}",
  }

  payload = {
      "model": "llama3-70b-8192",
      "messages": [
          {
              "role": "system",
              "content": (
                  "Jesteś analitykiem quant. Podaj krótki sygnał LONG/SHORT,"
                  " oraz konkretną cenę Stop Loss i Take Profit."
              ),
          },
          {
              "role": "user",
              "content": (
                  f"Aktywo: {aktywo}, Aktualna cena rynkowa:"
                  f" {aktualna_cena} PLN. Daj sygnał i poziomy SL/TP."
              ),
          },
      ],
      "temperature": 0.2,
  }

  try:
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        json=payload,
        headers=headers,
    )
    if response.status_code == 200:
      ai_data = response.json()
      odpowiedz_ai = ai_data["choices"][0]["message"]["content"]
      return jsonify({"sukces": True, "raport": odpowiedz_ai})
    else:
      return jsonify(
          {"sukces": False, "blad": "Błąd dostawcy AI w chmurze."}
      ), 500
  except Exception as e:
    return jsonify({"sukces": False, "blad": str(e)}), 500


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000)
