# backend/routes/health.py

from fastapi import APIRouter, HTTPException
from backend.routes.schemas import (
    PatientRequest, DiagnoseRequest,
    VitalsRequest, AdviceRequest
)
from backend.mcp_server.health_mcp_server import (
    diagnose_patient,
    get_patient_history,
    monitor_vitals,
    get_health_advice
)
import json

router = APIRouter(prefix="/api/health", tags=["health"])


@router.post("/diagnose")
async def diagnose(request: DiagnoseRequest):
    try:
        result = diagnose_patient(**request.model_dump())
        return json.loads(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/patient/{patient_id}")
async def patient_history(patient_id: str):
    try:
        result = get_patient_history(patient_id)
        return json.loads(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/vitals")
async def vitals(request: VitalsRequest):
    try:
        result = monitor_vitals(**request.model_dump())
        return json.loads(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/advice")
async def advice(request: AdviceRequest):
    try:
        result = get_health_advice(**request.model_dump())
        return json.loads(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/patients")
async def list_patients():
    from backend.data.patient_db import PATIENTS
    return {
        pid: {
            "name":   p["name"],
            "age":    p["age"],
            "gender": p["gender"]
        }
        for pid, p in PATIENTS.items()
    }