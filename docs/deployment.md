# Deployment Guide

## Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

For production:

- Use Azure App Service, Azure Container Apps, or Azure Kubernetes Service.
- Move secrets to Azure Key Vault.
- Replace SQLite with Azure SQL or PostgreSQL when multi-user scale is required.
- Enable managed identity so `DefaultAzureCredential` can access Foundry Agent Service.
- Configure CORS to the deployed frontend origin only.

## Frontend

```bash
cd frontend
npm install
npm run build
```

Set:

```bash
VITE_API_BASE_URL=https://<backend-host>
```

Deploy the `dist/` folder to Azure Static Web Apps, Azure App Service, or any static hosting service.

## OCR

The API includes `POST /ocr`. For local OCR, install Tesseract and optionally set `TESSERACT_CMD` in `backend/.env`.

For a production-grade Microsoft stack, replace `OCRService` with Azure AI Document Intelligence or Azure AI Vision Read OCR.
