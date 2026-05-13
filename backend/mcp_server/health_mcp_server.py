# backend/mcp_server/health_mcp_server.py

import sys
import os
sys.path.append(os.path.abspath("."))

import json
import joblib
import numpy as np
from mcp.server.fastmcp import FastMCP

from backend.data.patient_db import PATIENTS, HEALTHY_RANGES

# ── Load ML model & scaler once at startup ──────────────────────────────────
MODEL_PATH  = "backend/models/diabetes_model.pkl"
SCALER_PATH = "backend/models/scaler.pkl"

model  = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

FEATURE_ORDER = [
    "Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
    "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"
]

# ── Create MCP server ────────────────────────────────────────────────────────
mcp = FastMCP("HealthAssistantMCP")


# ── Tool 1: Diagnose patient ─────────────────────────────────────────────────
@mcp.tool()
def diagnose_patient(
    Pregnancies: float,
    Glucose: float,
    BloodPressure: float,
    SkinThickness: float,
    Insulin: float,
    BMI: float,
    DiabetesPedigreeFunction: float,
    Age: float
) -> str:
    """
    Predict diabetes risk for a patient based on their health metrics.
    Returns risk level (High/Low), probability, and a short clinical note.
    """
    features = np.array([[
        Pregnancies, Glucose, BloodPressure, SkinThickness,
        Insulin, BMI, DiabetesPedigreeFunction, Age
    ]])

    features_scaled = scaler.transform(features)
    prediction      = model.predict(features_scaled)[0]
    probability     = model.predict_proba(features_scaled)[0]

    risk_level  = "High" if prediction == 1 else "Low"
    confidence  = round(float(max(probability)) * 100, 2)

    # Simple clinical flags
    flags = []
    if Glucose > 140:
        flags.append("Elevated glucose (>140 mg/dL)")
    if BMI > 30:
        flags.append("Obese BMI (>30)")
    if BloodPressure > 90:
        flags.append("High blood pressure (>90 mmHg)")
    if Age > 45:
        flags.append("Age risk factor (>45 years)")

    result = {
        "risk_level":   risk_level,
        "confidence":   f"{confidence}%",
        "prediction":   "Diabetic" if prediction == 1 else "Non-Diabetic",
        "clinical_flags": flags if flags else ["No major flags detected"],
        "note": (
            "Immediate medical consultation recommended."
            if risk_level == "High"
            else "Continue healthy lifestyle monitoring."
        )
    }
    return json.dumps(result, indent=2)


# ── Tool 2: Get patient history ──────────────────────────────────────────────
@mcp.tool()
def get_patient_history(patient_id: str) -> str:
    """
    Retrieve a patient's medical history and past records by patient ID.
    Available IDs: P001, P002, P003
    """
    patient = PATIENTS.get(patient_id.upper())

    if not patient:
        return json.dumps({
            "error": f"Patient '{patient_id}' not found.",
            "available_ids": list(PATIENTS.keys())
        })

    return json.dumps({
        "patient_id":   patient_id.upper(),
        "name":         patient["name"],
        "age":          patient["age"],
        "gender":       patient["gender"],
        "total_records": len(patient["records"]),
        "records":      patient["records"]
    }, indent=2)


# ── Tool 3: Monitor vitals ───────────────────────────────────────────────────
@mcp.tool()
def monitor_vitals(
    Glucose: float,
    BloodPressure: float,
    BMI: float,
    Insulin: float,
    SkinThickness: float
) -> str:
    """
    Check if a patient's vitals are within healthy ranges.
    Returns a status report for each vital sign.
    """
    vitals = {
        "Glucose":       Glucose,
        "BloodPressure": BloodPressure,
        "BMI":           BMI,
        "Insulin":       Insulin,
        "SkinThickness": SkinThickness
    }

    report = {}
    overall_status = "Normal"

    for vital, value in vitals.items():
        healthy = HEALTHY_RANGES[vital]
        if value < healthy["min"]:
            status = "Low"
            overall_status = "Attention Required"
        elif value > healthy["max"]:
            status = "High"
            overall_status = "Attention Required"
        else:
            status = "Normal"

        report[vital] = {
            "value":         value,
            "unit":          healthy["unit"],
            "status":        status,
            "healthy_range": f"{healthy['min']} - {healthy['max']}"
        }

    return json.dumps({
        "overall_status": overall_status,
        "vitals_report":  report
    }, indent=2)


# ── Tool 4: Get health advice ────────────────────────────────────────────────
@mcp.tool()
def get_health_advice(risk_level: str, age: int, bmi: float) -> str:
    """
    Provide personalized health and lifestyle advice based on
    risk level, age, and BMI.
    """
    advice = []

    if risk_level.lower() == "high":
        advice += [
            "Consult an endocrinologist immediately.",
            "Monitor blood glucose levels daily.",
            "Follow a low-glycemic index diet.",
            "Avoid sugary drinks and processed foods.",
            "Exercise at least 30 minutes daily (walking, yoga).",
        ]
    else:
        advice += [
            "Maintain a balanced diet rich in fiber and vegetables.",
            "Stay physically active with regular moderate exercise.",
            "Get annual blood glucose screening.",
        ]

    if bmi > 30:
        advice.append("Work with a nutritionist to reduce BMI to healthy range (18.5–24.9).")
    elif bmi > 25:
        advice.append("Mild weight reduction recommended through diet and exercise.")

    if age > 45:
        advice.append("Increase screening frequency due to age-related risk factors.")

    return json.dumps({
        "risk_level":    risk_level,
        "advice_count":  len(advice),
        "advice":        advice
    }, indent=2)


# ── Run the server ───────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Starting Health Assistant MCP Server...")
    mcp.run(transport="stdio")