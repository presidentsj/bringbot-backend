
from flask import Flask, request, jsonify
import openai
import fitz  # PyMuPDF
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Charger et indexer le contenu PDF
def extraire_texte_du_pdf(fichier_pdf):
    doc = fitz.open(fichier_pdf)
    contenu = ""
    for page in doc:
        contenu += page.get_text()
    return contenu

pdf_texte = extraire_texte_du_pdf("catalogue_bring_negoce.pdf")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")

    if not message:
        return jsonify({"reply": "Message vide reçu."}), 400

    try:
        prompt = f"Voici un extrait d'un catalogue de matériaux :\n{pdf_texte[:2000]}\n\nQuestion : {message}\nRéponse :"
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un assistant commercial spécialisé dans la vente de matériaux de construction. Réponds aux questions en t'appuyant sur le catalogue fourni."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.4
        )
        reponse = completion.choices[0].message["content"].strip()
        return jsonify({"reply": reponse})
    except Exception as e:
        return jsonify({"reply": f"[Erreur serveur] {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
