# offer-sorter

A small backend that stores job postings, extracts useful information from them and compares them with
your own profile.

You paste in the text of a job posting and the API saves it in a PostgreSQL database. The goal is to
detect the technologies, the work mode (remote, hybrid or on-site) and the experience each posting asks
for, and to see how well it matches your skills. Postings are always added by hand: the project does not
scrape LinkedIn or any other job board.

## Status

The project is built in phases:

- [x] **Phase 1: Skeleton.** REST API with FastAPI, CRUD for job postings stored in PostgreSQL, and Docker Compose.
- [ ] **Phase 2: Rule-based extraction.** Technologies, work mode, languages and years of experience, using regular expressions.
- [ ] **Phase 3: Profile matching.** Compare each posting with a `profile.yaml`: what matches, what is missing and a score.
- [ ] **Phase 4: Analysis with pandas.** Most requested technologies, share of remote postings and salary ranges.
- [ ] **Phase 5 (optional): LLM extraction.** Extract the same fields with an LLM and compare the results with the rule-based ones.

## Tech stack

- Python 3.14 and [uv](https://docs.astral.sh/uv/) for dependencies
- FastAPI
- PostgreSQL 17 with SQLAlchemy 2.0
- pytest (the tests run on an in-memory SQLite database)
- Docker Compose
- Ruff for linting and formatting

## Getting started

### 1. Configure the environment

Copy the example file and set your own password:

```bash
cp .env.example .env
```

On Windows PowerShell, use `Copy-Item .env.example .env` instead.

Then open `.env` and replace `change-me` with a password of your choice. It appears twice, in
`POSTGRES_PASSWORD` and inside `DATABASE_URL`, and both must match. `.env` is git-ignored, so the
password is never committed.

### 2. Run everything with Docker

You only need [Docker](https://docs.docker.com/get-docker/) for this:

```bash
docker compose up --build
```

This starts two containers:

- `db`: PostgreSQL. Its data is kept in a named volume, so it survives `docker compose down`.
- `api`: the FastAPI app. It waits until the database is ready to accept connections before starting.

Open <http://localhost:8000/docs> to try the API from your browser.

### Run the API locally (development)

For development it is more convenient to run only the database in Docker and the API on your machine,
because the API then reloads every time you save a file. This needs uv:

```bash
uv sync
docker compose up -d db
uv run fastapi dev app/main.py
```

If the `api` container is running, stop it first with `docker compose stop api`, because both use port 8000.

## API

| Method | Path | Description | Success |
|---|---|---|---|
| `GET` | `/offers` | List all job postings | `200` |
| `GET` | `/offers/{offer_id}` | Get one job posting (`404` if it does not exist) | `200` |
| `POST` | `/offers` | Create a job posting | `201` |
| `DELETE` | `/offers/{offer_id}` | Delete a job posting (`404` if it does not exist) | `204` |

Example body for `POST /offers`:

```json
{
  "title": "Python Developer",
  "company": "Example Corp",
  "description": "Backend role with Python and FastAPI. 2+ years of experience. Fully remote.",
  "work_mode": "remote"
}
```

`work_mode` must be one of `onsite`, `remote` or `hybrid`. Any other value returns `422`.

## Tests and linting

```bash
uv run pytest
uv run ruff check
uv run ruff format --check
```

The tests replace the database dependency with an in-memory SQLite database (see `tests/conftest.py`),
so they do not need Docker or PostgreSQL. They do need a `.env` file (step 1), because the app reads
`DATABASE_URL` when it is imported.

## Project structure

```
app/
├── main.py         # FastAPI app; creates the tables on startup
├── config.py       # Settings read from environment variables / .env
├── database.py     # SQLAlchemy engine, session and the get_db dependency
├── models.py       # Database tables (SQLAlchemy models)
├── schemas.py      # Request and response bodies (Pydantic models)
└── routers/
    └── offers.py   # /offers endpoints
tests/
├── conftest.py     # In-memory SQLite database and sample postings
└── test_offers.py  # API tests
```

## License

[GPL-3.0](LICENSE)
