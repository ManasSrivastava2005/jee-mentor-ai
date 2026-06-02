# JEE Mentor AI

Full-stack AI reasoning agent for the Microsoft Agents League Hackathon 2026 Reasoning Agents track.

## Features

- Step-by-step JEE Physics, Chemistry, and Mathematics question solving.
- Topic detection returning `subject`, `topic`, and `confidence_score`.
- Foundry IQ knowledge retrieval with citations.
- Microsoft Foundry Agent Service orchestration.
- Similar question generation with Easy, Medium, and Hard variants.
- Weak topic tracker with history, analytics, and revision recommendations.
- OCR endpoint for handwritten or printed question images.
- React + Vite frontend and Python FastAPI backend.

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

## Run Locally

Backend:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

## API Endpoints

- `POST /solve`
- `POST /generate-similar`
- `POST /ocr`
- `GET /analytics`
- `GET /history`
- `GET /weak-topics`
- `GET /health`

## Database Tables

- `users`
- `questions`
- `topics`
- `performance`

## Foundry Setup

See [docs/foundry-iq-integration.md](docs/foundry-iq-integration.md).

## Deployment

See [docs/deployment.md](docs/deployment.md).

## Architecture

See [docs/architecture.md](docs/architecture.md).

## Demo

See [docs/demo-script.md](docs/demo-script.md).
