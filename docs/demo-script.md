# Hackathon Demo Script

## Opening

JEE Mentor AI is a reasoning agent for JEE aspirants. It combines Microsoft Foundry Agent Service, Foundry IQ retrieval, and a full-stack learning dashboard to solve questions and detect weak topics.

## Demo Flow

1. Open the React app.
2. Submit this question:

   `A point charge q is placed at the center of a cube. Find the electric flux through one face of the cube.`

3. Show topic detection:

   - Subject: Physics
   - Topic: Electrostatics
   - Confidence score

4. Show the step-by-step answer and formulas.
5. Point out citations from the Foundry IQ-backed JEE knowledge base.
6. Generate three similar questions across Easy, Medium, and Hard.
7. Upload an image of a printed question to show OCR support.
8. Open History to show stored solved questions.
9. Open Analytics to show most attempted topics, weak topics, and recommended revision areas.

## Closing

The project is production-oriented: modular FastAPI backend, React + Vite frontend, SQLite for the initial database, Foundry integration points, documentation, deployment guide, and a path to scale with Azure services.
