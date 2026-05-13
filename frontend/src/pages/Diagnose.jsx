// frontend/src/pages/Diagnose.jsx

import { useState } from "react";
import { diagnosePatient } from "../api";
import { Stethoscope } from "lucide-react";

const DEFAULTS = {
  Pregnancies: 3, Glucose: 148, BloodPressure: 72,
  SkinThickness: 35, Insulin: 0, BMI: 33.6,
  DiabetesPedigreeFunction: 0.627, Age: 45,
};

export default function Diagnose() {
  const [form,   setForm]   = useState(DEFAULTS);
  const [result, setResult] = useState(null);
  const [loading,setLoading]= useState(false);

  const update = (k, v) => setForm((f) => ({ ...f, [k]: parseFloat(v) || 0 }));

  const submit = async () => {
    setLoading(true);
    try {
      const r = await diagnosePatient(form);
      setResult(r.data);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1 className="page-title">Diagnose Patient</h1>
      <div className="grid-2" style={{ alignItems: "start" }}>

        {/* Form */}
        <div className="card">
          <h3>Enter Patient Vitals</h3>
          <div className="grid-2">
            {Object.entries(form).map(([k, v]) => (
              <div className="form-group" key={k}>
                <label>{k}</label>
                <input
                  type="number" step="any" value={v}
                  onChange={(e) => update(k, e.target.value)}
                />
              </div>
            ))}
          </div>
          <button className="btn btn-primary" onClick={submit} disabled={loading} style={{ width: "100%" }}>
            <Stethoscope size={15} style={{ marginRight: 6 }} />
            {loading ? "Diagnosing…" : "Run Diagnosis"}
          </button>
        </div>

        {/* Result */}
        <div className="card">
          <h3>Diagnosis Result</h3>
          {!result ? (
            <div style={{ color: "#a0aec0", textAlign: "center", padding: "40px 0" }}>
              Fill in the vitals and click Run Diagnosis
            </div>
          ) : (
            <div>
              <div style={{ textAlign: "center", marginBottom: 20 }}>
                <div style={{ fontSize: 48, marginBottom: 8 }}>
                  {result.risk_level === "High" ? "🔴" : "🟢"}
                </div>
                <div style={{ fontSize: 22, fontWeight: 700 }}>{result.prediction}</div>
                <span className={`badge badge-${result.risk_level === "High" ? "high" : "low"}`}>
                  {result.risk_level} Risk
                </span>
                <div style={{ marginTop: 8, color: "#718096", fontSize: 13 }}>
                  Confidence: {result.confidence}
                </div>
              </div>

              <div style={{ marginBottom: 16 }}>
                <div style={{ fontWeight: 600, marginBottom: 8, fontSize: 13 }}>Clinical Flags</div>
                {result.clinical_flags.map((f, i) => (
                  <div key={i} style={{
                    background: "#fff5f5", color: "#c53030",
                    padding: "6px 10px", borderRadius: 6,
                    fontSize: 13, marginBottom: 6
                  }}>⚠ {f}</div>
                ))}
              </div>

              <div style={{
                background: result.risk_level === "High" ? "#fff5f5" : "#f0fff4",
                padding: 12, borderRadius: 8, fontSize: 13,
                color: result.risk_level === "High" ? "#c53030" : "#276749"
              }}>
                📋 {result.note}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}