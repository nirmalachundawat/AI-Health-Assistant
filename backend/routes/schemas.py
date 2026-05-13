# backend/routes/schemas.py

from pydantic import BaseModel, Field
from typing import Optional

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"

class ChatResponse(BaseModel):
    response: str
    session_id: str

class PatientRequest(BaseModel):
    patient_id: str

class DiagnoseRequest(BaseModel):
    Pregnancies: float = Field(..., ge=0)
    Glucose: float     = Field(..., ge=0)
    BloodPressure: float = Field(..., ge=0)
    SkinThickness: float = Field(..., ge=0)
    Insulin: float       = Field(..., ge=0)
    BMI: float           = Field(..., ge=0)
    DiabetesPedigreeFunction: float = Field(..., ge=0)
    Age: float           = Field(..., ge=0)

class VitalsRequest(BaseModel):
    Glucose: float
    BloodPressure: float
    BMI: float
    Insulin: float
    SkinThickness: float

class AdviceRequest(BaseModel):
    risk_level: str
    age: int
    bmi: float