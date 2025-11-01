# 🧠 EFRN – Enterprise Financial Registry Network (POC)

### IBM Call for Code 2025 | watsonx Orchestrate + IBM FTM

EFRN is an **AI-orchestrated, bank-linked, portable financial identity system**  
designed to unify employee loans, payroll transactions, and global compliance.

---

## 🚀 Features
- Flask backend simulating IBM watsonx Orchestrate agents.
- React frontend dashboard showing live AI agent workflow.
- Blockchain-style local ledger for transaction immutability.
- Ethical and regulator-safe orchestration model.

---

## 🧩 Tech Stack
| Layer | Technology |
|-------|-------------|
| Backend | Python Flask |
| Frontend | React.js |
| Ledger | Local JSON + SHA256 Hash |
| AI Simulation | Mock Orchestrate YAML Agents |

---

## Overview
This POC demonstrates an orchestration pipeline with explainable agents (Compliance, Risk, Escrow, Settlement, Audit), a PLR ledger, and a human-in-loop override.


## ▶️ Run Locally


### Backend
1. Open terminal, go to `backend/` folder.
2. Create venv and install:
   ```bash
   python -m venv venv
   source venv/bin/activate    # or .\venv\Scripts\activate on Windows
   pip install -r requirements.txt