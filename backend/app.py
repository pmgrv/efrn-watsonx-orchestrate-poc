from flask import Flask, jsonify, request
from flask_cors import CORS
from orchestrate_api import orchestrate_transaction, manual_override
from pathlib import Path
import sys

# Add ledger path
sys.path.append(str(Path(__file__).resolve().parents[1] / "plr-ledger"))
from ledger_demo import get_recent_transactions

app = Flask(__name__)
CORS(app)

@app.route("/api/transaction", methods=["POST"])
def api_transaction():
    payload = request.get_json(force=True)
    result = orchestrate_transaction(payload)
    return jsonify(result)

@app.route("/api/ledger", methods=["GET"])
def api_ledger():
    ledger = get_recent_transactions(limit=20)
    # filter genesis / system blocks if any
    filtered = [tx for tx in ledger if tx.get("employee")]
    # newest first
    filtered = sorted(filtered, key=lambda x: x["timestamp"], reverse=True)
    return jsonify(filtered)

@app.route("/api/override", methods=["POST"])
def api_override():
    payload = request.get_json(force=True)
    result = manual_override(payload)
    return jsonify(result)

@app.route("/")
def index():
    return jsonify({"message": "EFRN-v2 backend running", "endpoint": "/api/transaction"})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)