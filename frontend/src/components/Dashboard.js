import React, { useState, useEffect } from "react";
import axios from "axios";

const API_BASE = "http://127.0.0.1:5000/api";

const Dashboard = () => {
  const [workflow, setWorkflow] = useState(null);
  const [ledger, setLedger] = useState([]);
  const [loading, setLoading] = useState(false);
  const [overrideModal, setOverrideModal] = useState(false);
  const [overrideForm, setOverrideForm] = useState({ employee: "", justification: "" });

  // fetch ledger data
  const fetchLedger = async () => {
    try {
      const res = await axios.get(`${API_BASE}/ledger`);
      setLedger(res.data);
    } catch (e) {
      console.error("Failed to fetch ledger:", e);
    }
  };

  useEffect(() => {
    fetchLedger();
  }, []);

  // run orchestration scenario
  const runScenario = async (isPositive) => {
    setLoading(true);
    setWorkflow(null);
    try {
      const payload = {
        employee: isPositive ? "EMP001" : "EMP999",
        amount: isPositive ? 1200 : 20000,
        currency: "USD",
        scenario: isPositive ? "positive" : "negative"
      };
      const res = await axios.post(`${API_BASE}/transaction`, payload);
      setWorkflow(res.data);
      await fetchLedger();
    } catch (e) {
      alert("Backend not reachable. Please ensure Flask server is running.");
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  // open override modal
  const openOverride = (employee) => {
    setOverrideForm({ employee, justification: "" });
    setOverrideModal(true);
  };

  // submit override request
  const submitOverride = async () => {
    const payload = {
      employee: overrideForm.employee,
      approver: "RISK_OFFICER",
      justification: overrideForm.justification,
      currency: "USD"
    };

    try {
      const res = await axios.post(`${API_BASE}/override`, payload); // ✅ fixed line
      if (res.data && res.data.finalStatus) {
        setWorkflow(res.data);
        alert("✅ Override applied successfully!");
      } else {
        alert("⚠️ Override API returned unexpected response.");
        console.log("Override response:", res.data);
      }
      setOverrideModal(false);
      await fetchLedger();
    } catch (e) {
      console.error("Override error:", e);
      alert("❌ Override failed — check backend logs.");
    }
  };

  // get background color per agent
	const getCardColor = (agent, status) => {
	  if (!status || status === "Pending")
		return { background: "#f2f2f2", border: "2px solid #ccc" };

	  const s = status.toLowerCase();

	  // Red for rejection/failure
	  if (s.includes("rejected") || s.includes("fail"))
		return { background: "#ffe5e5", border: "2px solid #ff4d4d" };

	  // Mint for overridden
	  if (agent === "Risk" && (s.includes("overridden") || s.includes("override")))
		return { background: "#c6f6d5", border: "2px solid #28a745" };

	  // Light green for cleared / verified / recorded
	  if (
		s.includes("cleared") ||
		s.includes("verified") ||
		s.includes("score") ||
		s.includes("held") ||
		s.includes("approved") ||
		s.includes("recorded")
	  )
		return { background: "#e8fbe8", border: "2px solid #28a745" };

	  // Neutral default
	  return { background: "#f2f2f2", border: "2px solid #ccc" };
	};


  const AGENTS = ["Compliance", "Risk", "Escrow", "Settlement", "Audit"];

  return (
    <div style={{ textAlign: "center", padding: "24px", fontFamily: "Arial, sans-serif" }}>
	{workflow && (
	  <div style={{ marginTop: 10, color: "#333" }}>
		<strong>EFRN ID:</strong> {workflow.efrn_id || "-"} |
		<strong> Trust Score:</strong> {workflow.trust_score_before || "-"}
	  </div>
	)}
      <h1 style={{ color: "#0043ce" }}>EFRN – AI Orchestrated Financial Trust Network</h1>
	
      {/* Run Scenarios */}
      <div style={{ margin: "16px" }}>
        <button
          onClick={() => runScenario(true)}
          disabled={loading}
          style={{
            marginRight: 10,
            padding: "10px 18px",
            background: "#0043ce",
            color: "white",
            border: "none",
            borderRadius: 8
          }}
        >
          {loading ? "Running..." : "Run Positive Scenario"}
        </button>

        <button
          onClick={() => runScenario(false)}
          disabled={loading}
          style={{
            padding: "10px 18px",
            background: "#c91414",
            color: "white",
            border: "none",
            borderRadius: 8
          }}
        >
          {loading ? "Running..." : "Run Negative Scenario"}
        </button>
      </div>

      {/* Agent Workflow Section */}
      <h2 style={{ marginTop: 18 }}>Agent Workflow</h2>
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))",
          gap: 18,
          justifyItems: "center",
          marginTop: 16
        }}
      >
        {AGENTS.map((agent) => {
          const step = workflow?.steps?.find((s) => s.agent === agent);
          const status = step ? step.status : "Pending";
          const color = getCardColor(agent, status);
          return (
           <div
			  key={agent}
			  style={{
				width: 220,
				borderRadius: 12,
				background: color.background,
				border: color.border,
				padding: 18,
				boxShadow: "0 2px 6px rgba(0,0,0,0.08)"
			  }}
			>
              <h4 style={{ color: "#0043ce", marginBottom: 8 }}>{agent}</h4>
              <div style={{ marginBottom: 6 }}>{status}</div>
              {step?.timestamp && <div style={{ fontSize: 12, color: "#444" }}>{step.timestamp}</div>}

              {/* Override button if Risk rejected */}
              {agent === "Risk" && status?.toLowerCase()?.includes("rejected") && (
                <div style={{ marginTop: 10 }}>
                  <button
                    onClick={() => openOverride(workflow?.employee)}
                    style={{
                      padding: "6px 10px",
                      borderRadius: 6,
                      border: "none",
                      background: "#0043ce",
                      color: "white"
                    }}
                  >
                    Override
                  </button>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Final Status */}
      {workflow && (
        <div style={{ marginTop: 18 }}>
          <h3
            style={{
              color:
                workflow.finalStatus?.toLowerCase() === "rejected" ? "red" : "green"
            }}
          >
            Final Status: {workflow.finalStatus}
          </h3>
          {workflow.reason && <p style={{ color: "red" }}>{workflow.reason}</p>}
        </div>
      )}

      {/* Ledger Table */}
      <h3 style={{ marginTop: 26 }}>Recent Transactions</h3>
      <div
        style={{
          width: "90%",
          margin: "10px auto",
          background: "white",
          boxShadow: "0 2px 8px rgba(0,0,0,0.08)"
        }}
      >
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr style={{ background: "#0043ce", color: "white" }}>
              <th style={{ padding: "10px" }}>Timestamp</th>
              <th>Employee</th>
              <th>Amount</th>
              <th>Currency</th>
              <th>Status</th>
              <th>Reason</th>
            </tr>
          </thead>
          <tbody>
            {ledger.map((tx, idx) => (
              <tr key={idx} style={{ textAlign: "center", borderBottom: "1px solid #eee" }}>
                <td style={{ padding: "8px" }}>{tx.timestamp}</td>
                <td>{tx.employee}</td>
                <td>{tx.amount}</td>
                <td>{tx.currency}</td>
                <td
				  style={{
					color:
					  tx.status?.toLowerCase() === "cleared"
						? "green"
						: tx.status?.toLowerCase() === "rejected"
						? "#d32f2f"
						: tx.status?.toLowerCase() === "cleared_by_override"
						? "#ff9800" // amber for manual override
						: "black",
					fontWeight: "500"
				  }}
				>
				  {tx.status}
				</td>

                <td style={{ textAlign: "left", padding: "8px" }}>
                  {tx.reason || "-"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Override Modal */}
      {overrideModal && (
        <div
          style={{
            position: "fixed",
            left: 0,
            top: 0,
            right: 0,
            bottom: 0,
            background: "rgba(0,0,0,0.4)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center"
          }}
        >
          <div style={{ background: "white", padding: 20, borderRadius: 8, width: 560 }}>
            <h3>Manual Override</h3>
            <div style={{ marginBottom: 8 }}>
              <label>Employee: </label>
              <input
                value={overrideForm.employee}
                readOnly
                style={{ width: "100%", padding: 8, marginTop: 6 }}
              />
            </div>
            <div style={{ marginBottom: 8 }}>
              <label>Justification</label>
              <textarea
                value={overrideForm.justification}
                onChange={(e) =>
                  setOverrideForm({ ...overrideForm, justification: e.target.value })
                }
                style={{ width: "100%", minHeight: 80, padding: 8, marginTop: 6 }}
              />
            </div>
            <div style={{ textAlign: "right" }}>
              <button
                onClick={() => setOverrideModal(false)}
                style={{ marginRight: 8, padding: "8px 12px" }}
              >
                Cancel
              </button>
              <button
                onClick={submitOverride}
                style={{
                  padding: "8px 12px",
                  background: "#0043ce",
                  color: "white",
                  border: "none"
                }}
              >
                Submit Override
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;