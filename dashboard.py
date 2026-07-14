from flask import Flask, render_template
import json
import os

app = Flask(__name__)

@app.route("/")
def index():
    if os.path.exists("metrics.json"):
        with open("metrics.json", "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    else:
        dados = {
            "status": "SEM DADOS",
            "node_id": "Nexus",
            "last_payload": "Nenhum",
            "timestamp": "-"
        }

    return render_template("index.html", dados=dados)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)