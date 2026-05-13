// frontend/src/pages/Vitals.jsx

import { useState } from "react";
import { monitorVitals } from "../api";
import { Activity } from "lucide-react";

const DEFAULTS = { Glucose: 120, BloodPressure: 80, BMI: 27.5, Insulin: 85, SkinThickness: 25 };

export default function Vitals() {
  const [form,   setForm]   = useState(DEFAULTS);
  const [result, setResult] = useState(null);
  const [loading,setLoading]= useState(false);

  const update = (k, v) => setForm((f) => ({ ...f, [k]: parseFloat(v) || 0 }));

  const submit = async () => {
    setLoading(true);
    try {
      const r = await monitorVitals(form);
      setResult(r.data);
    } finally {
      setLoading(false);
    }
  };

  const statusColor = (s) =>
    s === "Normal" ? "#276749" : s === "High" ? "#c53030" : "#744210";
  const statusBg = (s) =>
    s === "Normal" ? "#f0fff4" : s === "High" ? "#fff5f5" : "#fefcbf";

  return (
    <div>
      <h1 className="page-title">Vitals Monitor</h1>
      <div className="grid-2" style={{ alignItems: "start" }}>

        <div className="card">
          <h3>Enter Vital Signs</h3>
          {Object.entries(form).map(([k, v]) => (
            <div className="form-group" key={k}>
              <label>{k}</label>
              <input
                type="number" step="any" value={v}
                onChange={(e) => update(k, e.target.value)}
              />
            </div>
          ))}
          <button className="btn btn-primary" onClick={submit} disabled={loading} style={{ width: "100%" }}>
            <Activity size={15} style={{ marginRight: 6 }} />
            {loading ? "Checking…" : "Check Vitals"}
          </button>
        </div>

        <div className="card">
          <h3>Vitals Report</h3>
          {!result ? (
            <div style={{ color: "#a0aec0", textAlign: "center", padding: "40px 0" }}>
              Enter vitals and click Check Vitals
            </div>
          ) : (
            <div>
              <div style={{ textAlign: "center", marginBottom: 20 }}>
                <span className={`badge badge-${result.overall_status === "Normal" ? "normal" : "warn"}`}
                  style={{ fontSize: 14, padding: "6px 16px" }}>
                  Overall: {result.overall_status}
                </span>
              </div>
              {Object.entries(result.vitals_report).map(([vital, info]) => (
                <div key={vital} style={{
                  background: statusBg(info.status),
                  border: `1px solid ${statusColor(info.status)}22`,
                  borderRadius: 8, padding: "12px 14px", marginBottom: 10
                }}>
                  <div style={{ display: "flex", justifyContent: "space-between" }}>
                    <span style={{ fontWeight: 600, fontSize: 14 }}>{vital}</span>
                    <span style={{
                      fontWeight: 700, color: statusColor(info.status), fontSize: 14
                    }}>
                      {info.status}
                    </span>
                  </div>
                  <div style={{ fontSize: 13, color: "#4a5568", marginTop: 4 }}>
                    Value: <b>{info.value} {info.unit}</b> · Healthy: {info.healthy_range}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}