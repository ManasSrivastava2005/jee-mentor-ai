# JEE Mentor AI

An AI-powered learning assistant built for the Agents League Hackathon 2026. JEE Mentor AI helps students solve JEE-level Physics, Chemistry, and Mathematics questions, identify weak topics, track learning progress, and receive intelligent study support through a modern AI-driven platform.

## Problem Statement

JEE aspirants often struggle to identify weak concepts, understand solution steps, and maintain consistent revision. Most learning platforms provide answers but lack personalized reasoning and performance insights.

JEE Mentor AI addresses this by combining question solving, topic detection, analytics, OCR-based question input, and personalized performance tracking in a single platform.

---

## Key Features

### AI Question Solver

* Step-by-step solution generation
* Subject and topic detection
* Confidence scoring
* Formula-based reasoning

### Learning Analytics

* Weak topic identification
* Performance tracking
* Question history
* Revision recommendations

### OCR Question Input

* Upload handwritten or printed questions
* Automatic text extraction
* Direct solving workflow

### Similar Question Generation

* Easy, Medium, and Hard variants
* Practice-focused learning

### Knowledge Retrieval Layer

* Retrieval-augmented architecture
* Citation-aware responses
* Local knowledge base support
* Ready for Microsoft Foundry IQ integration

---

## Architecture

```text
React + Vite Frontend
          |
          v
      FastAPI API
          |
  ------------------
  |       |        |
Solver  Analytics  OCR
Engine   Engine   Service
  |
Knowledge Retrieval
  |
SQLite Database
```

---

## Technology Stack

### Frontend

* React
* Vite

### Backend

* FastAPI
* Python

### Database

* SQLite
* SQLAlchemy

### AI Components

* Topic Detection Engine
* Solver Registry Architecture
* Knowledge Retrieval System
* Analytics Engine

---

## Project Structure

```text
frontend/
backend/
  app/
    agents/
    api/
    services/
    models/
    database/
    utils/
docs/
knowledge-base/
README.md
```

---

## Running Locally

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
copy .env.example .env
.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open:

http://localhost:5173

---

## API Endpoints

| Endpoint          | Method | Purpose                     |
| ----------------- | ------ | --------------------------- |
| /solve            | POST   | Solve JEE questions         |
| /generate-similar | POST   | Generate practice questions |
| /ocr              | POST   | OCR extraction              |
| /analytics        | GET    | Student analytics           |
| /history          | GET    | Question history            |
| /weak-topics      | GET    | Weak topic analysis         |
| /health           | GET    | Service health check        |

---

## Current Capabilities

* Topic classification
* Electrostatics reasoning
* Question history tracking
* OCR pipeline
* Learning analytics
* Similar question generation
* Weak-topic detection

---

## Future Roadmap

* Advanced Physics solvers
* Calculus solver engine
* Coordinate Geometry solver
* Personalized study planner
* Mock test generation
* Cloud deployment
* Full Microsoft Foundry IQ integration

---

## Screenshots

### Question Solver

![Question Solver](docs/screenshots/chat.png)

### Analytics Dashboard

![Analytics Dashboard](docs/screenshots/analytics.png)

### History Page

![History Page](docs/screenshots/history.png)

---


## Hackathon Submission

**Hackathon:** Agents League 2026

**Track:** Reasoning Agents

**Developer:** Manas Srivastava

---

## Demo

See `docs/demo-script.md` for demonstration workflow.
