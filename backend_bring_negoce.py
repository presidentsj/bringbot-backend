
from flask import Flask, request, jsonify
import openai
import fitz  # PyMuPDF
import os

app = Flask(__name__)

# Configuration : à remplacer par ta propre clé API
openai.api_key = "VOTRE_CLE_API_ICI"

# Lecture du contenu PDF à intégrer
def extract_pdf_content(pdf_path):
    content = ""
    try:
        with fitz.open(pdf_path) as doc:
            for page in doc:
                content += page.get_text()
        return content[:3000]  # Limiter à 3000 caractères pour éviter surcharge
    except Exception as e:
        return f"Erreur de lecture PDF : {e}"

PDF_KNOWLEDGE = extract_pdf_content("catalogue_bring_negoce.pdf")

@app.route("/api/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"Tu es l'assistant de Bring Négoce. Tu utilises les informations suivantes extraites du catalogue PDF pour aider les visiteurs :\n{PDF_KNOWLEDGE}"},
                {"role": "user", "content": user_input}
            ]
        )
        reply = response.choices[0].message["content"]
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
