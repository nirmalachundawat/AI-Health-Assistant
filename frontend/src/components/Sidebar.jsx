// frontend/src/components/Sidebar.jsx

import { Activity, MessageSquare, Users, Stethoscope, Heart } from "lucide-react";

const navItems = [
  { id: "chat",     label: "AI Chat",    icon: MessageSquare },
  { id: "patients", label: "Patients",   icon: Users },
  { id: "diagnose", label: "Diagnose",   icon: Stethoscope },
  { id: "vitals",   label: "Vitals",     icon: Activity },
];

export default function Sidebar({ active, onChange }) {
  return (
    <div className="sidebar">
      <div className="sidebar-logo">
        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <Heart size={20} color="#63b3ed" fill="#63b3ed" />
          <h2>HealthAI</h2>
        </div>
        <p>AI Health Assistant</p>
      </div>
      <nav className="sidebar-nav">
        {navItems.map(({ id, label, icon: Icon }) => (
          <div
            key={id}
            className={`nav-item ${active === id ? "active" : ""}`}
            onClick={() => onChange(id)}
          >
            <Icon size={16} />
            {label}
          </div>
        ))}
      </nav>
      <div style={{ padding: "16px 24px", fontSize: 11, color: "#718096" }}>
        Powered by Groq + Claude
      </div>
    </div>
  );
}