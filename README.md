# Recipe Hub

Recipe Hub is a React recipe application. A FastAPI backend is being introduced
alongside the existing Express and MongoDB backend.

## Current Stack

- React
- Vite
- Tailwind CSS
- FastAPI
- Express
- MongoDB / Mongoose
- AWS S3 for recipe images

## Running Locally

### Frontend

```sh
npm install
npm run dev
```

### FastAPI backend

```sh
cd backend
python -m venv .venv
```

Activate the virtual environment on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

Then install and run the API:

```sh
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

The health endpoint is available at `http://localhost:8000/health` and the
interactive API documentation at `http://localhost:8000/docs`.

The React app reads the FastAPI URL from `VITE_FASTAPI_URL`, which defaults to
`http://localhost:8000`. Copy `.env.example` to `.env` to override it.

### Existing Express backend

```sh
cd server
npm install
npm start
```

The Express backend requires environment variables defined in `server/.env`.

See `server/.env.example` for the required variables.

## Project Status

This project is currently being refactored and rebuilt into a voice-powered RAG cooking assistant.
