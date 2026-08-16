# JEE Mentor AI 🤖

> An AI-powered JEE learning assistant that helps students solve questions, understand concepts, identify weak topics, and track their learning progress.

![Python](https://img.shields.io/badge/Python-3.x-blue)
![React](https://img.shields.io/badge/React-Vite-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey)
![Status](https://img.shields.io/badge/Status-Active%20Development-orange)

JEE Mentor AI is an AI-powered learning platform built for the **Agents League Hackathon 2026**. It combines question solving, topic detection, OCR-based question input, learning analytics, question history, and personalized practice into a single platform for JEE aspirants.

---

## 🎯 Problem Statement

JEE aspirants often struggle with more than simply finding the correct answer.

Students need to understand:

- Why a particular solution works
- Which concepts they repeatedly struggle with
- What topics require revision
- How to practice effectively after solving a question
- How their performance changes over time

Many learning platforms provide answers but do not provide enough personalized reasoning or performance insights.

**JEE Mentor AI** addresses this gap by combining intelligent question solving, topic detection, OCR, analytics, question history, and similar-question generation into one learning workflow.

---

## 💡 Why JEE Mentor AI?

JEE Mentor AI is designed around the idea that **solving a question is only one part of learning**.

The platform helps students:

- Understand solution steps
- Identify weak topics
- Practice similar questions
- Track question history
- Analyze learning performance
- Convert handwritten or printed questions into digital input
- Build a more personalized revision workflow

---

## ✨ Key Features

### 🧠 AI Question Solver

- Step-by-step solution generation
- JEE-oriented question solving
- Subject and topic detection
- Confidence scoring
- Formula-based reasoning
- Structured reasoning workflow

### 📊 Learning Analytics

- Weak-topic identification
- Performance tracking
- Question history
- Learning statistics
- Revision recommendations

### 📷 OCR Question Input

- Upload handwritten or printed questions
- Extract question text using OCR
- Send extracted questions directly to the solving workflow
- Reduce manual typing for students

### 📝 Similar Question Generation

Generate additional practice questions based on the original problem.

Supports:

- Easy
- Medium
- Hard

This allows students to immediately practice the same concept at different difficulty levels.

### 🔎 Knowledge Retrieval Layer

- Retrieval-augmented architecture
- Citation-aware responses
- Local knowledge-base support
- Modular retrieval design
- Architecture prepared for future Microsoft Foundry IQ integration

### 📚 Learning History

Students can review previously solved questions and use their history to identify recurring problem areas.

---

## 🏗️ Architecture

```text
                    React + Vite
                         │
                         ▼
                   FastAPI Backend
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
   Solver Engine     Analytics        OCR Service
        │                │                │
        └────────────────┼────────────────┘
                         │
                         ▼
               Knowledge Retrieval
                         │
                         ▼
                  SQLite Database
```

The backend is designed using modular services so that additional subject solvers, retrieval systems, and AI capabilities can be added without restructuring the entire application.

---

## 🛠️ Technology Stack

### Frontend

- React
- Vite
- JavaScript
- CSS

### Backend

- Python
- FastAPI
- REST APIs

### Database

- SQLite
- SQLAlchemy

### AI & Learning Components

- Topic Detection Engine
- Solver Registry Architecture
- Knowledge Retrieval System
- Analytics Engine
- OCR Pipeline
- Similar Question Generation

### Development Tools

- Git
- GitHub
- VS Code
- Python Virtual Environment

---

## 📁 Project Structure

```text
JEE-Mentor-AI/
│
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
│
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   ├── api/
│   │   ├── services/
│   │   ├── models/
│   │   ├── database/
│   │   └── utils/
│   │
│   ├── requirements.txt
│   └── .env.example
│
├── docs/
│   ├── screenshots/
│   └── demo-script.md
│
├── knowledge-base/
│
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

Make sure you have the following installed:

- Python 3.x
- Node.js
- npm
- Git

### 1. Clone the repository

```bash
git clone https://github.com/ManasSrivastava2005/JEE-Mentor-AI.git
cd JEE-Mentor-AI
```

### 2. Set up the backend

```bash
cd backend
python -m venv .venv
```

#### Windows

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

#### Configure environment variables

Create a `.env` file based on `.env.example`:

```text
copy .env.example .env
```

Add the required configuration values to `.env`.

> ⚠️ Never commit your actual `.env` file, API keys, credentials, or other secrets to GitHub.

### 3. Start the backend

```powershell
.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

The FastAPI backend will normally be available at:

```text
http://127.0.0.1:8000
```

### 4. Set up the frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:5173
```

---

## 🔐 Environment Variables

The backend uses environment variables for configuration and sensitive credentials.

Example:

```env
# Server
PORT=8000

# Database
DATABASE_URL=your_database_configuration

# AI / External Services
API_KEY=your_api_key
```

> The exact variables required depend on the services enabled in the project. Use `.env.example` as the source of truth.

**Never commit real credentials or API keys to GitHub.**

---

## 🔌 API Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/solve` | POST | Solve JEE questions |
| `/generate-similar` | POST | Generate similar practice questions |
| `/ocr` | POST | Extract text from uploaded questions |
| `/analytics` | GET | Retrieve student analytics |
| `/history` | GET | Retrieve question history |
| `/weak-topics` | GET | Identify weak topics |
| `/health` | GET | Check backend health |

---

## 📈 Current Capabilities

The current implementation includes:

- ✅ Topic classification
- ✅ JEE question-solving workflow
- ✅ Electrostatics reasoning
- ✅ Question history tracking
- ✅ OCR pipeline
- ✅ Learning analytics
- ✅ Similar-question generation
- ✅ Weak-topic detection
- ✅ Modular solver architecture
- ✅ Knowledge retrieval architecture

---

## 🧪 Example Learning Workflow

```text
Student
   │
   ▼
Enter / Upload Question
   │
   ├── Text Input
   └── OCR Input
   │
   ▼
Question Analysis
   │
   ├── Subject Detection
   ├── Topic Detection
   └── Difficulty / Confidence
   │
   ▼
AI Solver
   │
   ▼
Step-by-Step Explanation
   │
   ├── Save to History
   ├── Update Analytics
   └── Identify Weak Topics
   │
   ▼
Generate Similar Questions
   │
   ▼
Practice & Improve
```

---

## 📸 Screenshots

### Question Solver

![Question Solver](docs/screenshots/chat.png)

### Analytics Dashboard

![Analytics Dashboard](docs/screenshots/analytics.png)

### Question History

![History Page](docs/screenshots/History.png)

> Make sure these screenshot files exist at the paths above before publishing the repository.

---

## 🎥 Demo

A complete demonstration workflow is available in:

```text
docs/demo-script.md
```

The demo covers:

1. Opening the application
2. Entering a JEE question
3. Generating a solution
4. Viewing analytics
5. Checking question history
6. Identifying weak topics
7. Generating similar questions
8. Testing the OCR workflow

---

## 📌 Project Status

🟢 **Active Development**

The core solving, OCR, analytics, question-history, similar-question, and weak-topic workflows are implemented.

Future development will focus on expanding subject coverage, improving personalization, adding additional solver modules, and deploying the platform to the cloud.

---

## 🗺️ Roadmap

### 🔬 AI & Solving

- [ ] Advanced Physics solver coverage
- [ ] Chemistry reasoning engine
- [ ] Calculus solver engine
- [ ] Coordinate Geometry solver
- [ ] Advanced multi-step reasoning
- [ ] Improved confidence estimation

### 📚 Learning

- [ ] Personalized study planner
- [ ] Adaptive revision scheduling
- [ ] Mock test generation
- [ ] Personalized difficulty progression
- [ ] Topic-wise performance visualization

### ☁️ Infrastructure

- [ ] Cloud deployment
- [ ] Production database
- [ ] Docker containerization
- [ ] CI/CD pipeline
- [ ] Production monitoring

### 🤖 AI Integrations

- [ ] Microsoft Foundry IQ integration
- [ ] Expanded knowledge retrieval
- [ ] Improved citation-aware responses
- [ ] Personalized AI tutoring

---

## 🏆 Hackathon Submission

**Hackathon:** Agents League Hackathon 2026

**Track:** Reasoning Agents

**Project:** JEE Mentor AI

**Developer:** Manas Srivastava

JEE Mentor AI was developed as a reasoning-focused educational AI system designed to help JEE aspirants solve questions while also understanding their learning patterns and weak areas.

---

## 🔮 Future Vision

The long-term goal of JEE Mentor AI is to evolve from a question-solving tool into a **personalized AI learning companion for competitive-exam students**.

Future versions could continuously analyze a student's:

- Solved questions
- Weak concepts
- Practice history
- Difficulty progression
- Revision patterns
- Subject performance

and use this information to create a personalized learning experience.

---

## 👨‍💻 Author

### Manas Srivastava

**CSE — Cloud Computing & Automation**  
**VIT Bhopal University**

GitHub: [@ManasSrivastava2005](https://github.com/ManasSrivastava2005)

---

## 📄 License

This project is currently developed as an educational and portfolio project.
```
