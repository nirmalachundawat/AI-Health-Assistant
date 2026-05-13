#### AI Health Assistant
### Agentic AI System for Diabetes Diagnosis & Disease Monitoring

## 📌 Table of Contents

1. [Project Overview](#-project-overview)
2. [Features](#-features)
3. [Tech Stack](#-tech-stack)
4. [System Architecture](#-system-architecture)
5. [Agentic AI Workflow](#-agentic-ai-workflow)
6. [Project Structure](#-project-structure)
7. [Dataset](#-dataset)
8. [ML Model](#-ml-model)
9. [MCP Tools](#-mcp-tools)
10. [API Reference](#-api-reference)
11. [Environment Setup](#-environment-setup)
12. [Installation](#-installation)
13. [Running the Project](#-running-the-project)
14. [Frontend UI Guide](#-frontend-ui-guide)
15. [Testing](#-testing)
16. [Troubleshooting](#-troubleshooting)
17. [Future Roadmap](#-future-roadmap)

---

## 🧠 Project Overview

**AI Health Assistant** is a fully agentic AI application that uses a Large Language Model (LLM) at its core to intelligently diagnose diabetes risk and monitor patient health — powered by real machine learning, structured tools, and a conversational interface.

Unlike a simple chatbot, this system is **agentic** — meaning the AI autonomously decides which tools to call, in what order, and how to interpret results to provide a complete, medically-informed response to the user.

The system is built on the **Model Context Protocol (MCP)** pattern, where the LLM is given a set of typed tools it can invoke during reasoning. This allows the AI to:

- Fetch real patient data before making decisions
- Run an ML model to predict diabetes risk
- Check vitals against medical healthy ranges
- Give personalized lifestyle advice based on diagnosis

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 💬 **AI Health Chat** | Natural language conversation with the health agent |
| 🩺 **Diabetes Diagnosis** | ML-powered risk prediction from patient vitals |
| 👥 **Patient Management** | View and manage patient records and history |
| 📊 **Vitals Monitoring** | Real-time vital signs analysis vs healthy ranges |
| 💡 **Health Advice** | Personalized lifestyle and medical recommendations |
| 🔄 **Multi-turn Memory** | Agent remembers context across the conversation |
| 🛠️ **Tool Orchestration** | LLM autonomously chains multiple tools per query |
| 🌐 **REST API** | Full FastAPI backend with Swagger documentation |
| ⚡ **One-click Startup** | Launch entire stack with a single `.bat` file |

---

## 🏗 System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER (Browser)                           │
└──────────────────────────┬──────────────────────────────────────┘
                           │ HTTP requests
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                 React Frontend (port 3000)                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐   │
│  │   Chat   │  │ Patients │  │ Diagnose │  │    Vitals    │   │
│  │   Page   │  │   Page   │  │   Page   │  │     Page     │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────────┘   │
└──────────────────────────┬──────────────────────────────────────┘
                           │ REST API (JSON)
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                  FastAPI Backend (port 8000)                     │
│                                                                  │
│   /api/chat  ──────────────────────► HealthAgent                │
│   /api/health/diagnose ────────────► Direct Tool Call           │
│   /api/health/patient/{id} ────────► Direct Tool Call           │
│   /api/health/vitals ──────────────► Direct Tool Call           │
│   /api/health/advice ──────────────► Direct Tool Call           │
│   /api/health/patients ────────────► Patient Database           │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                      HealthAgent Core                            │
│                                                                  │
│   conversation_history ──► Groq LLM (llama-3.3-70b)            │
│                                  │                              │
│                            stop_reason?                         │
│                           /          \                          │
│                     tool_use         end_turn                   │
│                        │                │                       │
│                   run_tool()        return text                  │
│                        │                                        │
│              ┌─────────┴──────────┐                            │
│              │    MCP Tool Map    │                             │
│              ├───────────────────-┤                             │
│              │ diagnose_patient   │──► Random Forest Model      │
│              │ get_patient_history│──► Patient Database         │
│              │ monitor_vitals     │──► Healthy Ranges Config    │
│              │ get_health_advice  │──► Rule-based Advice Engine │
│              └────────────────────┘                             │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Agentic AI Workflow

This is what happens internally when a user sends a message like:
> *"Diagnose patient P001 and give me health advice"*

```
Step 1: User message received
        │
        ▼
Step 2: Message added to conversation_history
        │
        ▼
Step 3: Full history sent to Groq LLM with tool definitions
        │
        ▼
Step 4: LLM decides → stop_reason = "tool_calls"
        LLM picks: get_patient_history(patient_id="P001")
        │
        ▼
Step 5: tool_runner.py executes get_patient_history("P001")
        Returns: Aisha Sharma's records (JSON)
        │
        ▼
Step 6: Tool result added to conversation_history
        History sent back to LLM again
        │
        ▼
Step 7: LLM decides → stop_reason = "tool_calls"
        LLM picks: diagnose_patient(Glucose=148, BMI=33.6, ...)
        │
        ▼
Step 8: tool_runner.py executes diagnose_patient(...)
        ML model runs → Returns: High Risk, 82% confidence
        │
        ▼
Step 9: Tool result added to history
        History sent back to LLM again
        │
        ▼
Step 10: LLM decides → stop_reason = "tool_calls"
         LLM picks: get_health_advice(risk_level="High", age=45, bmi=33.6)
         │
         ▼
Step 11: Returns personalized advice list
         │
         ▼
Step 12: LLM decides → stop_reason = "stop"
         LLM synthesizes ALL tool results into a
         coherent, empathetic medical response
         │
         ▼
Step 13: Final response returned to FastAPI → React → User
```

This entire loop happens **automatically** — the LLM decides how many tools to call and in what order, with no hardcoded logic.

---

## 📁 Project Structure

```
ai-health-assistant/
│
├── 📂 backend/
│   ├── __init__.py
│   ├── main.py                          ← FastAPI app entry point + CORS
│   │
│   ├── 📂 agent/
│   │   ├── __init__.py
│   │   ├── config.py                    ← API keys, model name, system prompt
│   │   ├── health_agent.py              ← Core agentic loop (tool orchestration)
│   │   ├── tool_definitions.py          ← Tool schemas exposed to the LLM
│   │   └── tool_runner.py               ← Executes tools by name
│   │
│   ├── 📂 mcp_server/
│   │   ├── __init__.py
│   │   ├── health_mcp_server.py         ← 4 MCP tools implementation
│   │   └── test_tools.py                ← Tool unit tests
│   │
│   ├── 📂 data/
│   │   ├── __init__.py
│   │   ├── download_data.py             ← Downloads PIMA dataset from GitHub
│   │   ├── preprocess.py                ← Cleans data, fits/saves scaler
│   │   ├── patient_db.py                ← Mock patient records + healthy ranges
│   │   └── diabetes.csv                 ← PIMA Indians Diabetes Dataset
│   │
│   ├── 📂 models/
│   │   ├── __init__.py
│   │   ├── train_model.py               ← Trains and saves Random Forest model
│   │   ├── diabetes_model.pkl           ← Saved trained ML model
│   │   └── scaler.pkl                   ← Saved StandardScaler
│   │
│   └── 📂 routes/
│       ├── __init__.py
│       ├── schemas.py                   ← Pydantic request/response models
│       ├── chat.py                      ← /api/chat endpoint + session management
│       └── health.py                    ← /api/health/* direct tool endpoints
│
├── 📂 frontend/
│   ├── public/
│   └── src/
│       ├── index.js                     ← React entry point
│       ├── index.css                    ← Global styles
│       ├── App.js                       ← Root component + routing
│       ├── api.js                       ← Axios API service layer
│       │
│       ├── 📂 components/
│       │   └── Sidebar.jsx              ← Navigation sidebar
│       │
│       └── 📂 pages/
│           ├── Chat.jsx                 ← AI chat interface
│           ├── Patients.jsx             ← Patient list + history viewer
│           ├── Diagnose.jsx             ← Diagnosis form + result display
│           └── Vitals.jsx               ← Vitals monitoring form + report
│
├── venv/                                ← Python virtual environment
├── .env                                 ← API keys (never commit this!)
├── requirements.txt                     ← Python dependencies
├── start.bat                            ← One-click startup script (Windows)
├── stop.bat                             ← One-click shutdown script (Windows)
└── README.md                            ← This file
```

---

## 📊 Dataset

**PIMA Indians Diabetes Dataset**

- **Source:** National Institute of Diabetes and Digestive and Kidney Diseases
- **Hosted:** [Jason Brownlee's GitHub](https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv)
- **Rows:** 768 patient records
- **Target:** Binary classification (0 = Non-Diabetic, 1 = Diabetic)

## 🤖 ML Model

**Algorithm:** Random Forest Classifier

```
Parameters:
  n_estimators = 100
  max_depth    = 6
  random_state = 42
  class_weight = "balanced"

Performance:
  Accuracy     ~ 78-82%
  Train size   = 614 samples
  Test size    = 154 samples
```

### Why Random Forest?
- Handles mixed feature types well
- Robust to outliers in medical data
- Provides probability scores (confidence %)
- No need for extensive hyperparameter tuning
- Interpretable feature importance

---

## 🔧 MCP Tools

The agent has access to 4 tools defined in `health_mcp_server.py`:

### 1. `diagnose_patient`
Runs the ML model on patient vitals and returns risk assessment.

**Input:**
```json
{
  "Pregnancies": 3,
  "Glucose": 148,
  "BloodPressure": 72,
  "SkinThickness": 35,
  "Insulin": 0,
  "BMI": 33.6,
  "DiabetesPedigreeFunction": 0.627,
  "Age": 45
}
```

**Output:**
```json
{
  "risk_level": "High",
  "confidence": "82.00%",
  "prediction": "Diabetic",
  "clinical_flags": ["Elevated glucose (>140 mg/dL)", "Obese BMI (>30)"],
  "note": "Immediate medical consultation recommended."
}
```

---

### 2. `get_patient_history`
Retrieves a patient's full medical records from the database.

**Input:** `{ "patient_id": "P001" }`

**Output:** Patient name, age, gender, all past records with dates.

---

### 3. `monitor_vitals`
Checks each vital against established healthy ranges.

**Healthy Ranges Used:**
| Vital | Min | Max | Unit |
|-------|-----|-----|------|
| Glucose | 70 | 100 | mg/dL |
| BloodPressure | 60 | 80 | mmHg |
| BMI | 18.5 | 24.9 | kg/m² |
| Insulin | 16 | 166 | mu U/ml |
| SkinThickness | 10 | 40 | mm |

---

### 4. `get_health_advice`
Returns personalized advice based on risk level, age, and BMI.

**Logic:**
- High risk → clinical intervention advice
- Low risk → preventive lifestyle advice
- BMI > 30 → nutritionist referral added
- Age > 45 → increased screening frequency added

---

## 📡 API Reference

Base URL: `http://localhost:8000`

### Chat Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/chat` | Send message to AI agent |
| POST | `/api/chat/reset` | Reset conversation session |

**POST /api/chat**
```json
Request:
{
  "message": "Get history for patient P001",
  "session_id": "user-123"
}

Response:
{
  "response": "Here is the medical history for Aisha Sharma...",
  "session_id": "user-123"
}
```

---

### Health Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health/patients` | List all patients |
| GET | `/api/health/patient/{id}` | Get patient history |
| POST | `/api/health/diagnose` | Run diabetes diagnosis |
| POST | `/api/health/vitals` | Monitor vital signs |
| POST | `/api/health/advice` | Get health advice |
| GET | `/health` | Server health check |
| GET | `/docs` | Swagger UI documentation |

---

## ⚙️ Environment Setup

### Prerequisites

| Tool | Version | Download |
|------|---------|----------|
| Python | 3.11.x | [python.org](https://python.org) |
| Node.js | 18+ | [nodejs.org](https://nodejs.org) |
| Git | Any | [git-scm.com](https://git-scm.com) |

### API Keys Required

| Service | Purpose | Get Key |
|---------|---------|---------|
| Groq | LLM (free) | [console.groq.com](https://console.groq.com) |

---

## 📦 Installation

### Step 1 — Clone or create the project folder
```bash
mkdir ai-health-assistant
cd ai-health-assistant
```

### Step 2 — Create Python virtual environment
```bash
py -3.11 -m venv venv
venv\Scripts\activate
```

### Step 3 — Install Python dependencies
```bash
pip install --upgrade pip
pip install numpy --only-binary=:all:
pip install pandas --only-binary=:all:
pip install scikit-learn --only-binary=:all:
pip install anthropic fastapi uvicorn python-dotenv joblib httpx pydantic python-multipart mcp groq
```

### Step 4 — Set up environment variables
Create `.env` in the project root:
```env
GROQ_API_KEY=gsk_actual_key_here
```

### Step 5 — Download dataset and train model
```bash
python backend/data/download_data.py
python backend/models/train_model.py
```

### Step 6 — Install frontend dependencies
```bash
cd frontend
npm install
cd ..
```

---

## ▶️ Running the Project

### Option A — One-click startup (Recommended)
```bash
# Double-click this file in File Explorer:
start.bat
```

This automatically opens two terminal windows and launches both servers.

### Option B — Manual startup

**Terminal 1 — Backend:**
```bash
cd ai-health-assistant
venv\Scripts\activate
uvicorn backend.main:app --reload --port 8000
```

**Terminal 2 — Frontend:**
```bash
cd ai-health-assistant\frontend
npm start
```

### Access Points

| Service | URL |
|---------|-----|
| 🌐 Frontend App | http://localhost:3000 |
| ⚡ Backend API | http://localhost:8000 |
| 📖 API Docs (Swagger) | http://localhost:8000/docs |

### Shutdown
```bash
# Double-click:
stop.bat
```

---

## 🖥 Frontend UI Guide

### 💬 Chat Page
The main conversational interface. The AI agent autonomously calls tools based on our message.

**Example queries:**
```
"Get history for patient P001"
"Diagnose: Glucose=166, BMI=38.5, Age=52, BloodPressure=74, Pregnancies=5, SkinThickness=29, Insulin=0, DPF=0.587"
"What health advice for a high risk patient aged 45 with BMI 33?"
"Monitor vitals for Glucose=166, BloodPressure=90, BMI=35, Insulin=0, SkinThickness=30"
```

### 👥 Patients Page
View all registered patients. Click any patient card to expand their full medical history with all past records.

**Test Patient IDs:**
| ID | Name | Age | Gender |
|----|------|-----|--------|
| P001 | Aisha Sharma | 45 | Female |
| P002 | Rahul Verma | 32 | Male |
| P003 | Priya Patel | 52 | Female |

### 🩺 Diagnose Page
Enter patient vitals manually and get an instant ML-powered diagnosis with:
- Risk level (High / Low)
- Confidence percentage
- Clinical flags
- Recommendation note

### 📊 Vitals Page
Check individual vital signs against healthy medical ranges. Each vital shows:
- Current value vs healthy range
- Status: Normal / High / Low 
- Overall health status

---

## 🧪 Testing

### Test backend tools directly
```bash
python backend/mcp_server/test_tools.py
```

### Test agent standalone
```bash
python backend/agent/health_agent.py
```

### Test API endpoints (PowerShell)

```powershell
# Health check
Invoke-RestMethod -Uri "http://localhost:8000/health" -Method GET

# List patients
Invoke-RestMethod -Uri "http://localhost:8000/api/health/patients" -Method GET

# Get patient history
Invoke-RestMethod -Uri "http://localhost:8000/api/health/patient/P001" -Method GET

# Diagnose patient
Invoke-RestMethod -Uri "http://localhost:8000/api/health/diagnose" `
  -Method POST -ContentType "application/json" `
  -Body '{"Pregnancies":5,"Glucose":166,"BloodPressure":74,"SkinThickness":29,"Insulin":0,"BMI":38.5,"DiabetesPedigreeFunction":0.587,"Age":52}'

# Monitor vitals
Invoke-RestMethod -Uri "http://localhost:8000/api/health/vitals" `
  -Method POST -ContentType "application/json" `
  -Body '{"Glucose":166,"BloodPressure":74,"BMI":38.5,"Insulin":0,"SkinThickness":29}'

# AI Chat
Invoke-RestMethod -Uri "http://localhost:8000/api/chat" `
  -Method POST -ContentType "application/json" `
  -Body '{"message":"Diagnose patient P003","session_id":"test"}'
```

---

## 🚀 Future Roadmap

### Phase 2 — Enhanced Medical Coverage
- [ ] Heart disease risk prediction (Cleveland Heart Disease dataset)
- [ ] Hypertension detection model
- [ ] Multiple disease monitoring dashboard

### Phase 3 — Data & Persistence
- [ ] PostgreSQL database for real patient records
- [ ] User authentication (JWT tokens)
- [ ] Patient registration and login portal

### Phase 4 — Analytics
- [ ] Patient health trend charts (Chart.js / Recharts)
- [ ] Risk progression over time visualization
- [ ] Exportable PDF diagnosis reports

### Phase 5 — Production
- [ ] Docker containerization
- [ ] Deploy backend on Railway / Render
- [ ] Deploy frontend on Vercel / Netlify
- [ ] CI/CD pipeline with GitHub Actions

### Phase 6 — Advanced AI
- [ ] RAG (Retrieval-Augmented Generation) on medical literature
- [ ] Voice input for patient vitals
- [ ] Multi-language support (Hindi, etc.)

---

## 👨‍💻 Built With

This project was built step-by-step as a learning exercise covering:

- **Agentic AI design** — autonomous tool-calling loop
- **MCP pattern** — structured tool definitions for LLMs
- **FastAPI** — modern async Python web framework
- **React** — component-based frontend UI
- **Machine Learning** — end-to-end model training and inference
- **Full-stack integration** — connecting all layers into one working system

---

<div align="center">

**🏥 AI Health Assistant** — Built with ❤️ using Groq, FastAPI & React

*Remember: Always consult a licensed physician for medical decisions.*

</div>
