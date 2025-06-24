
from flask import Flask, request, jsonify
from flask_cors import CORS
import fitz  # PyMuPDF
import openai
import os

app = Flask(__name__)
CORS(app)

# Clé API OpenAI (à remplacer si besoin)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Lecture du PDF une seule fois au démarrage
def extraire_texte_du_pdf(fichier_pdf):
    doc = fitz.open(fichier_pdf)
    texte = ""
    for page in doc:
        texte += page.get_text()
    return texte

pdf_texte = extraire_texte_du_pdf("catalogue_bring_negoce.pdf")

@app.route("/api/chat", methods=["POST"])
def chatbot():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"reply": "Message vide."}), 400

    prompt = f"""Tu es un assistant virtuel pour l'entreprise Bring Négoce, spécialisée dans le négoce de matériaux BTP.
Voici le contenu du catalogue PDF de l'entreprise :

{pdf_texte}

Réponds à la question suivante de manière professionnelle et concise :
{user_message}"""

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        reply = completion.choices[0].message["content"]
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": f"[Erreur serveur] {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
