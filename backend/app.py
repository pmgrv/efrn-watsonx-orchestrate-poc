from flask import Flask, jsonify, request
from flask_cors import CORS
from orchestrate_api import orchestrate_transaction, manual_override
from pathlib import Path
import sys, os

# ----------------------------
# Dynamically import plr-ledger
# ----------------------------
ledger_path = os.path.join(os.path.dirname(__file__), "..", "plr-ledger")
sys.path.append(ledger_path)
import ledger_demo as ledger  # unified reference name

# ----------------------------
# Flask App
# ----------------------------
app = Flask(__name__)
CORS(app)

# ----------------------------
# Orchestration APIs
# ----------------------------
@app.route("/api/transaction", methods=["POST"])
def api_transaction():
    payload = request.get_json(force=True)
    result = orchestrate_transaction(payload)
    return jsonify(result)


@app.route("/api/ledger", methods=["GET"])
def api_ledger():
    ledger_data = ledger.get_recent_transactions(limit=20)
    filtered = [tx for tx in ledger_data if tx.get("employee") and tx["employee"] != "SYSTEM"]
    filtered = sorted(filtered, key=lambda x: x["timestamp"], reverse=True)
    return jsonify(filtered)


@app.route("/api/override", methods=["POST"])
def api_override():
    payload = request.get_json(force=True)
    result = manual_override(payload)
    return jsonify(result)

# ----------------------------
# 🔐 EFRN Digital ID APIs
# ----------------------------
@app.route("/api/efrn/profiles", methods=["GET"])
def get_efrn_profiles():
    """Return all persisted EFRN Digital IDs"""
    try:
        profiles = ledger.load_profiles()
        return jsonify(profiles)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/efrn/profile/<employee_code>", methods=["GET"])
def get_efrn_profile(employee_code):
    """Fetch a single EFRN profile"""
    profile = ledger.get_profile_by_employee(employee_code)
    if not profile:
        return jsonify({"error": "Profile not found"}), 404
    return jsonify(profile)


@app.route("/api/efrn/update/<employee_code>", methods=["POST"])
def update_efrn_profile(employee_code):
    """Update EFRN trust or wallet attributes manually"""
    data = request.get_json(force=True)
    delta = data.get("trust_delta", 0)
    try:
        ledger.update_trust_score(employee_code, delta)
        return jsonify({"message": f"EFRN profile for {employee_code} updated"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ----------------------------
# Root Check
# ----------------------------
@app.route("/")
def index():
    return jsonify({
        "message": "EFRN Digital ID Orchestrator backend running ✅",
        "routes": ["/api/transaction", "/api/ledger", "/api/efrn/profiles"]
    })

# ----------------------------
# Run Server
# ----------------------------
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)