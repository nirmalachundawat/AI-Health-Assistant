# backend/agent/tool_definitions.py

# These tell Claude what tools are available and how to call them

TOOLS = [
    {
        "name": "diagnose_patient",
        "description": (
            "Predict diabetes risk for a patient using their health metrics. "
            "Returns risk level (High/Low), confidence percentage, prediction, "
            "clinical flags, and a recommendation note."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "Pregnancies":             {"type": "number", "description": "Number of pregnancies (0 for males)"},
                "Glucose":                 {"type": "number", "description": "Plasma glucose concentration (mg/dL)"},
                "BloodPressure":           {"type": "number", "description": "Diastolic blood pressure (mmHg)"},
                "SkinThickness":           {"type": "number", "description": "Triceps skin fold thickness (mm)"},
                "Insulin":                 {"type": "number", "description": "2-Hour serum insulin (mu U/ml)"},
                "BMI":                     {"type": "number", "description": "Body mass index (weight in kg / height in m²)"},
                "DiabetesPedigreeFunction":{"type": "number", "description": "Diabetes pedigree function score"},
                "Age":                     {"type": "number", "description": "Age in years"},
            },
            "required": [
                "Pregnancies", "Glucose", "BloodPressure", "SkinThickness",
                "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"
            ]
        }
    },
    {
        "name": "get_patient_history",
        "description": (
            "Retrieve a patient's full medical history and past records "
            "using their patient ID. Available IDs: P001, P002, P003."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "patient_id": {
                    "type": "string",
                    "description": "Patient ID e.g. P001, P002, P003"
                }
            },
            "required": ["patient_id"]
        }
    },
    {
        "name": "monitor_vitals",
        "description": (
            "Check whether a patient's vital signs are within healthy ranges. "
            "Returns a status report (Normal / High / Low) for each vital."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "Glucose":       {"type": "number", "description": "Blood glucose level (mg/dL)"},
                "BloodPressure": {"type": "number", "description": "Diastolic blood pressure (mmHg)"},
                "BMI":           {"type": "number", "description": "Body mass index"},
                "Insulin":       {"type": "number", "description": "Serum insulin level (mu U/ml)"},
                "SkinThickness": {"type": "number", "description": "Skin fold thickness (mm)"},
            },
            "required": ["Glucose", "BloodPressure", "BMI", "Insulin", "SkinThickness"]
        }
    },
    {
        "name": "get_health_advice",
        "description": (
            "Get personalized health and lifestyle advice based on "
            "a patient's risk level, age, and BMI."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "risk_level": {
                    "type": "string",
                    "description": "Risk level: 'High' or 'Low'"
                },
                "age": {
                    "type": "integer",
                    "description": "Patient age in years"
                },
                "bmi": {
                    "type": "number",
                    "description": "Patient BMI value"
                }
            },
            "required": ["risk_level", "age", "bmi"]
        }
    }
]