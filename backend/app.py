from flask import Flask, jsonify, request
from flask_cors import CORS
from orchestrate_api import orchestrate_transaction
from pathlib import Path
import sys

# Add ledger path
sys.path.append(str(Path(__file__).resolve().parents[1] / "plr-ledger"))
from ledger_demo import get_recent_transactions

app = Flask(__name__)
CORS(app)

@app.route("/api/transaction", methods=["POST"])
def api_transaction():
    data = request.get_json(force=True)
    result = orchestrate_transaction(data)
    return jsonify(result)

@app.route("/api/ledger", methods=["GET"])
def api_ledger():
    ledger = get_recent_transactions(limit=10)

    # 🧹 Filter out the Genesis Block (no employee or system entries)
    filtered_ledger = [
        tx for tx in ledger
        if tx.get("employee") and tx.get("employee") not in ("SYSTEM", "")
    ]

    # 🕒 Sort by timestamp (most recent first)
    filtered_ledger = sorted(
        filtered_ledger, key=lambda x: x["timestamp"], reverse=True
    )

    return jsonify(filtered_ledger)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)