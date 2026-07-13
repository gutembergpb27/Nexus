from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

@app.route('/')
def index():
    if os.path.exists('metrics.json'):
        with open('metrics.json', 'r') as f:
            data = json.load(f)
        return jsonify(data)
    return "Métricas não encontradas", 404

if __name__ == '__main__':
    app.run(port=5000)