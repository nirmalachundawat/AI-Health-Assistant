# backend/data/patient_db.py

# Mock patient database — simulates real patient records
PATIENTS = {
    "P001": {
        "name": "Aisha Sharma",
        "age": 45,
        "gender": "Female",
        "records": [
            {
                "date": "2024-01-10",
                "Pregnancies": 3,
                "Glucose": 148,
                "BloodPressure": 72,
                "SkinThickness": 35,
                "Insulin": 0,
                "BMI": 33.6,
                "DiabetesPedigreeFunction": 0.627,
                "Age": 45
            },
            {
                "date": "2024-06-15",
                "Pregnancies": 3,
                "Glucose": 155,
                "BloodPressure": 76,
                "SkinThickness": 36,
                "Insulin": 0,
                "BMI": 34.1,
                "DiabetesPedigreeFunction": 0.627,
                "Age": 45
            }
        ]
    },
    "P002": {
        "name": "Rahul Verma",
        "age": 32,
        "gender": "Male",
        "records": [
            {
                "date": "2024-03-20",
                "Pregnancies": 0,
                "Glucose": 89,
                "BloodPressure": 66,
                "SkinThickness": 23,
                "Insulin": 94,
                "BMI": 28.1,
                "DiabetesPedigreeFunction": 0.167,
                "Age": 32
            }
        ]
    },
    "P003": {
        "name": "Priya Patel",
        "age": 52,
        "gender": "Female",
        "records": [
            {
                "date": "2024-02-05",
                "Pregnancies": 5,
                "Glucose": 166,
                "BloodPressure": 74,
                "SkinThickness": 29,
                "Insulin": 0,
                "BMI": 38.5,
                "DiabetesPedigreeFunction": 0.587,
                "Age": 52
            }
        ]
    }
}

HEALTHY_RANGES = {
    "Glucose":        {"min": 70,  "max": 100,  "unit": "mg/dL"},
    "BloodPressure":  {"min": 60,  "max": 80,   "unit": "mmHg"},
    "BMI":            {"min": 18.5,"max": 24.9,  "unit": "kg/m²"},
    "Insulin":        {"min": 16,  "max": 166,  "unit": "mu U/ml"},
    "SkinThickness":  {"min": 10,  "max": 40,   "unit": "mm"},
}