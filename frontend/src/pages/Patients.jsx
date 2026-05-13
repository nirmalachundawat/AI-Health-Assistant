// frontend/src/pages/Patients.jsx

import { useEffect, useState } from "react";
import { getPatients, getPatientHistory } from "../api";
import { User, ChevronDown, ChevronUp } from "lucide-react";

export default function Patients() {
  const [patients, setPatients]   = useState({});
  const [expanded, setExpanded]   = useState(null);
  const [history,  setHistory]    = useState({});

  useEffect(() => {
    getPatients().then((r) => setPatients(r.data));
  }, []);

  const toggle = async (pid) => {
    if (expanded === pid) { setExpanded(null); return; }
    setExpanded(pid);
    if (!history[pid]) {
      const r = await getPatientHistory(pid);
      setHistory((h) => ({ ...h, [pid]: r.data }));
    }
  };

  return (
    <div>
      <h1 className="page-title">Patients</h1>
      {Object.entries(patients).map(([pid, p]) => (
        <div className="card" key={pid} style={{ marginBottom: 12 }}>
          <div
            style={{ display: "flex", justifyContent: "space-between", alignItems: "center", cursor: "pointer" }}
            onClick={() => toggle(pid)}
          >
            <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
              <div style={{
                width: 42, height: 42, borderRadius: "50%",
                background: "#ebf8ff", display: "flex",
                alignItems: "center", justifyContent: "center"
              }}>
                <User size={20} color="#3182ce" />
              </div>
              <div>
                <div style={{ fontWeight: 600 }}>{p.name}</div>
                <div style={{ fontSize: 13, color: "#718096" }}>
                  {pid} · {p.gender} · Age {p.age}
                </div>
              </div>
            </div>
            {expanded === pid ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
          </div>

          {expanded === pid && history[pid] && (
            <div style={{ marginTop: 16 }}>
              <div style={{ fontSize: 13, fontWeight: 600, color: "#4a5568", marginBottom: 10 }}>
                Medical Records ({history[pid].total_records})
              </div>
              {history[pid].records.map((rec, i) => (
                <div key={i} style={{
                  background: "#f7fafc", borderRadius: 8,
                  padding: 14, marginBottom: 10, fontSize: 13
                }}>
                  <div style={{ fontWeight: 600, marginBottom: 8, color: "#2d3748" }}>
                    📅 {rec.date}
                  </div>
                  <div className="grid-3">
                    {Object.entries(rec)
                      .filter(([k]) => k !== "date")
                      .map(([k, v]) => (
                        <div key={k}>
                          <span style={{ color: "#718096" }}>{k}: </span>
                          <span style={{ fontWeight: 500 }}>{v}</span>
                        </div>
                      ))}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}