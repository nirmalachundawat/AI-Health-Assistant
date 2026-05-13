// frontend/src/api.js

import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:8000",
  headers: { "Content-Type": "application/json" },
});

// Chat
export const sendMessage = (message, session_id = "default") =>
  API.post("/api/chat", { message, session_id });

export const resetChat = (session_id = "default") =>
  API.post(`/api/chat/reset?session_id=${session_id}`);

// Health tools
export const getPatients = () =>
  API.get("/api/health/patients");

export const getPatientHistory = (patient_id) =>
  API.get(`/api/health/patient/${patient_id}`);

export const diagnosePatient = (data) =>
  API.post("/api/health/diagnose", data);

export const monitorVitals = (data) =>
  API.post("/api/health/vitals", data);

export const getAdvice = (data) =>
  API.post("/api/health/advice", data);