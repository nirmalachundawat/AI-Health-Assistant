#### AI Health Assistant
### Agentic AI System for Diabetes Diagnosis & Disease Monitoring

## Table of Contents

1. [Project Overview](#-project-overview)
2. [Dataset](#-dataset)
3. [Environment Setup](#-environment-setup)
4. [Installation](#-installation)
5. [Running the Project](#-running-the-project)
6. [Limitations](#-limitations)

---

## Project Overview

**AI Health Assistant** is a fully agentic AI application that uses a Large Language Model (LLM) at its core to intelligently diagnose diabetes risk and monitor patient health — powered by real machine learning, structured tools, and a conversational interface.

Unlike a simple chatbot, this system is **agentic** — meaning the AI autonomously decides which tools to call, in what order, and how to interpret results to provide a complete, medically-informed response to the user.

The system is built on the **Model Context Protocol (MCP)** pattern, where the LLM is given a set of typed tools it can invoke during reasoning. This allows the AI to:

- Fetch real patient data before making decisions
- Run an ML model to predict diabetes risk
- Check vitals against medical healthy ranges
- Give personalized lifestyle advice based on diagnosis

---

---

## Dataset

**PIMA Indians Diabetes Dataset**

- **Source:** National Institute of Diabetes and Digestive and Kidney Diseases
- **Hosted:** [Jason Brownlee's GitHub](https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv)
- **Rows:** 768 patient records
- **Target:** Binary classification (0 = Non-Diabetic, 1 = Diabetic)

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

## Environment Setup

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

## Installation

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

## Running the Project

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
----
## Limitations

- Mock patient database with only 3 hardcoded patients — no real data persistence.
- ML model trained only on diabetes data — no support for other diseases.
- ~78-82% model accuracy makes it unsuitable for real clinical decisions.
- No user authentication — not compliant with healthcare data privacy standards.
- Free Groq API tier has rate limits, causing occasional delays under heavy usage.
----
<div align="center">

*Remember: Always consult a licensed physician for medical decisions.*

</div>
