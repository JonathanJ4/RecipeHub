# Recipe Hub

Recipe Hub is a React recipe application backed by FastAPI and PostgreSQL.

## Current Stack

- React
- Vite
- Tailwind CSS
- FastAPI
- PostgreSQL / SQLAlchemy
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
uv sync
uv run fastapi dev
```

`uv sync` creates the project environment and installs the locked dependencies.
No manual virtual-environment activation is required.

### PostgreSQL

Create the backend environment file and start PostgreSQL from the project root:

```sh
cp backend/.env.example backend/.env
docker compose up -d postgres
```

Check that the database container is healthy:

```sh
docker compose ps
```

PostgreSQL is available locally on port `5432`. Its data is retained in the
`postgres_data` Docker volume. The FastAPI health endpoint checks the database
with a lightweight query and reports `"database": "online"` when connected.

Apply database schema migrations from the `backend` directory:

```sh
uv run alembic upgrade head
```

The current schema stores each recipe in one `recipes` table. Ingredients are
stored as PostgreSQL JSONB and instructions as text.

Import the Kaggle recipe dataset into an empty `recipes` table:

```sh
uv run python -m scripts.import_recipes
```

The importer ignores the CSV's exported index column, stores the original
`Ingredients` lists as JSONB, skips incomplete rows, and aborts if the table
already contains data.

To stop PostgreSQL without deleting its data:

```sh
docker compose stop postgres
```

The health endpoint is available at `http://localhost:8000/health` and the
interactive API documentation at `http://localhost:8000/docs`.

### Recipe API endpoints

- `GET /recipes?limit=20&offset=0` returns a paginated recipe list.
- `GET /recipes/{id}` returns one recipe or `404` when it is missing.
- `GET /recipes/search?q=chicken&limit=20&offset=0` searches titles,
  instructions, and ingredients without case sensitivity.
- `GET /images/{image_name}.jpg` serves recipe images from FastAPI.

The React app reads the FastAPI URL from `VITE_API_URL`, which defaults to
`http://localhost:8000`. Copy `.env.example` to `.env` to override it.

## Project Status

This project is currently being refactored and rebuilt into a voice-powered RAG cooking assistant.
