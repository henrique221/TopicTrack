from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.get_json()
    title = data.get('title', '')
    text = data.get('text', '')
    option = data.get('option', 's')
    print(data)

    if not text:
        return jsonify({"error": "O texto não pode estar vazio."}), 400

    # Chame sua função de resumo aqui e passe os parâmetros necessários
    # Exemplo: summary = summarize_text(text, title, option)
    summary = "Exemplo de resumo"  # Substitua esta linha pela chamada à sua função

    return jsonify({"summary": summary})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
