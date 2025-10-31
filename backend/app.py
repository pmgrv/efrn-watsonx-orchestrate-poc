from flask import Flask, jsonify, request
from flask_cors import CORS
from orchestrate_api import orchestrate_transaction

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})   # ✅ allow all origins for demo

@app.route("/")
def index():
    return jsonify({"message": "EFRN Backend Running", "endpoint": "/api/transaction"})

@app.route("/api/transaction", methods=["POST"])
def api_transaction():
    data = request.get_json(force=True)
    result = orchestrate_transaction(data)
    return jsonify(result)

if __name__ == "__main__":
    # Force IPv4 localhost to avoid mixed-address issues on Windows
    app.run(host="127.0.0.1", port=5000, debug=True)