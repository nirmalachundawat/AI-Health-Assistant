// frontend/src/pages/Chat.jsx

import { useState, useRef, useEffect } from "react";
import { sendMessage, resetChat } from "../api";
import { Send, RefreshCw, Bot, User } from "lucide-react";

export default function Chat() {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      text: "👋 Hello! I'm your AI Health Assistant. I can help you:\n\n• Diagnose diabetes risk from patient vitals\n• Look up patient history (try: 'Get history for P001')\n• Monitor vital signs\n• Give personalized health advice\n\nHow can I help you today?",
    },
  ]);
  const [input, setInput]     = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef             = useRef(null);
  const SESSION               = "chat-session-1";

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const send = async () => {
    if (!input.trim() || loading) return;
    const userMsg = input.trim();
    setInput("");
    setMessages((m) => [...m, { role: "user", text: userMsg }]);
    setLoading(true);

    try {
      const res = await sendMessage(userMsg, SESSION);
      setMessages((m) => [...m, { role: "assistant", text: res.data.response }]);
    } catch (e) {
      setMessages((m) => [...m, {
        role: "assistant",
        text: "⚠️ Error connecting to the server. Please try again.",
      }]);
    } finally {
      setLoading(false);
    }
  };

  const reset = async () => {
    await resetChat(SESSION);
    setMessages([{
      role: "assistant",
      text: "Chat reset! How can I help you?",
    }]);
  };

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <h1 className="page-title">AI Health Chat</h1>
        <button className="btn btn-danger btn-sm" onClick={reset}>
          <RefreshCw size={13} style={{ marginRight: 4 }} />
          Reset Chat
        </button>
      </div>

      {/* Suggestions */}
      <div style={{ display: "flex", gap: 8, marginBottom: 16, flexWrap: "wrap" }}>
        {[
          "Get history for patient P001",
          "Diagnose: Glucose=148, BMI=33.6, Age=45, BP=72, Pregnancies=3, SkinThickness=35, Insulin=0, DPF=0.627",
          "Health advice for high risk patient aged 52 with BMI 38",
        ].map((s) => (
          <button
            key={s}
            className="btn btn-sm"
            style={{ background: "#ebf8ff", color: "#2b6cb0", border: "1px solid #bee3f8" }}
            onClick={() => setInput(s)}
          >
            {s.length > 40 ? s.slice(0, 40) + "…" : s}
          </button>
        ))}
      </div>

      {/* Messages */}
      <div className="card" style={{ height: 420, overflowY: "auto", padding: 16 }}>
        {messages.map((m, i) => (
          <div
            key={i}
            style={{
              display: "flex",
              gap: 10,
              marginBottom: 16,
              flexDirection: m.role === "user" ? "row-reverse" : "row",
            }}
          >
            <div style={{
              width: 32, height: 32, borderRadius: "50%", flexShrink: 0,
              background: m.role === "user" ? "#3182ce" : "#1a365d",
              display: "flex", alignItems: "center", justifyContent: "center"
            }}>
              {m.role === "user"
                ? <User size={16} color="white" />
                : <Bot  size={16} color="white" />}
            </div>
            <div style={{
              maxWidth: "75%",
              background: m.role === "user" ? "#3182ce" : "#f7fafc",
              color: m.role === "user" ? "white" : "#2d3748",
              padding: "10px 14px",
              borderRadius: m.role === "user" ? "16px 4px 16px 16px" : "4px 16px 16px 16px",
              fontSize: 14,
              lineHeight: 1.6,
              whiteSpace: "pre-wrap",
              boxShadow: "0 1px 2px rgba(0,0,0,0.08)",
            }}>
              {m.text}
            </div>
          </div>
        ))}
        {loading && (
          <div style={{ display: "flex", gap: 10, marginBottom: 16 }}>
            <div style={{
              width: 32, height: 32, borderRadius: "50%",
              background: "#1a365d",
              display: "flex", alignItems: "center", justifyContent: "center"
            }}>
              <Bot size={16} color="white" />
            </div>
            <div style={{
              background: "#f7fafc", padding: "10px 14px",
              borderRadius: "4px 16px 16px 16px", fontSize: 14, color: "#718096"
            }}>
              Thinking…
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <div style={{ display: "flex", gap: 10, marginTop: 12 }}>
        <input
          style={{
            flex: 1, padding: "12px 16px", borderRadius: 8,
            border: "1px solid #e2e8f0", fontSize: 14, outline: "none"
          }}
          placeholder="Ask about a patient, diagnosis, or health advice…"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && send()}
        />
        <button className="btn btn-primary" onClick={send} disabled={loading}>
          <Send size={16} />
        </button>
      </div>
    </div>
  );
}