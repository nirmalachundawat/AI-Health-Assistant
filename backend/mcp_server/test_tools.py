# backend/mcp_server/test_tools.py

import sys, os
sys.path.append(os.path.abspath("."))

from backend.mcp_server.health_mcp_server import (
    diagnose_patient,
    get_patient_history,
    monitor_vitals,
    get_health_advice
)
import json

print("=" * 50)
print("TEST 1: Diagnose Patient")
print("=" * 50)
result = diagnose_patient(
    Pregnancies=3, Glucose=148, BloodPressure=72,
    SkinThickness=35, Insulin=0, BMI=33.6,
    DiabetesPedigreeFunction=0.627, Age=45
)
print(result)

print("\n" + "=" * 50)
print("TEST 2: Patient History")
print("=" * 50)
print(get_patient_history("P001"))

print("\n" + "=" * 50)
print("TEST 3: Monitor Vitals")
print("=" * 50)
print(monitor_vitals(
    Glucose=148, BloodPressure=72,
    BMI=33.6, Insulin=0, SkinThickness=35
))

print("\n" + "=" * 50)
print("TEST 4: Health Advice")
print("=" * 50)
print(get_health_advice("High", age=45, bmi=33.6))