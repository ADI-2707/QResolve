# QResolve

> An enterprise-style, multi-tenant support ticket platform with an AI-assisted priority prediction engine — built with FastAPI, SQLAlchemy, React (TypeScript), and scikit-learn.

---

## Overview

QResolve is a support-desk platform that lets organizations create tickets, assign them to agents, track their lifecycle, and automatically predict ticket **priority** using a trained machine learning model. It is architected as **multi-tenant SaaS**: every organization operates in a fully isolated workspace (its own users, tickets, departments, analytics, and audit trail) while sharing the same underlying infrastructure.

The system is made up of four components:

- **Frontend** — React + TypeScript (Vite)
- **Backend API** — FastAPI
- **Machine Learning Engine** — scikit-learn / TF-IDF based priority classifier
- **Database** — SQLAlchemy ORM (SQLite by default, PostgreSQL-ready)


Design principles (see [`docs/architecture/`](docs/architecture) for the full specs):

Design principles:


- **Multi-tenancy** — organizations can never access another organization's data; isolation is enforced in the backend on every query.
- **Enterprise-first** — the first experience is authentication, not marketing; every feature is built with security, auditing, and maintainability in mind.
- **AI-assisted, not AI-only** — the ML model predicts ticket priority, but agents can always review and override predictions.

---

## Features

### Ticketing & workflow
- Full ticket lifecycle: create, update, assign, claim, resolve, archive
- Status (`OPEN`, `IN_PROGRESS`, `RESOLVED`, `CLOSED`, `ARCHIVED`), priority (`LOW`–`CRITICAL`), and category (`TECHNICAL`, `BILLING`, `ACCOUNT`, `FEATURE_REQUEST`, `BUG`, `OTHER`) tracking
- Departments for routing/organizing tickets
- Threaded comments per ticket

### Multi-tenant organizations

- Organization creation, lookup by ID or slug
- Organization creation via **bootstrap** flow (new organization + first admin account)
- Organization lookup by ID or slug
- Memberships with role-based access: `PLATFORM_ADMIN`, `ORGANIZATION_ADMIN`, `MANAGER`, `AGENT`, `VIEWER`
- Email-based invitations with token-hashed, expiring invite links
- Suspend / activate members, change member roles

### Authentication & security
- Argon2 password hashing
- JWT access tokens (org ID, org slug, and role embedded in the token claims)
- Organization bootstrap flow (create org + first admin) and invitation-acceptance flow
- Organization bootstrap flow and invitation-acceptance flow
- Role-based authorization enforced at the endpoint level (`require_role`)

### AI-powered prediction
- Ticket priority prediction from ticket text + metadata (type, queue, tags)
- Per-ticket prediction endpoint plus a manual **override** endpoint so agents can correct the model
- Prediction history stored with confidence score, model version, and override tracking

### Observability & reporting
- Organization-scoped audit log (who did what, when, to what entity)
- Analytics endpoint for ticket overview stats
- Structured application logging (requests, predictions, DB ops, exceptions) to `logs/`

### Frontend
- React + TypeScript SPA (Vite) with a dedicated design-token system (colors, spacing, typography)
- Login page, Dashboard (stats cards, priority overview, recent tickets), Tickets page with filtering
- Login page with "Create organization" button
- Organization bootstrap page (create org + first admin account)
- Dashboard (stats cards, priority overview, recent tickets)
- Tickets page with filtering and management
- Members page for invitation and role management
- Audit logs page for security tracking
- Shared UI component library (Button, Card, Badge, Input, Navbar, Sidebar)

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11, TypeScript |
| Backend framework | FastAPI, Uvicorn, Pydantic |
| Auth | Argon2 (`argon2-cffi`), JWT (`python-jose`) |
| ORM / Migrations | SQLAlchemy, Alembic |
| Database | SQLite (default), PostgreSQL-ready (`psycopg2-binary`) |
| Machine Learning | scikit-learn, pandas, NumPy, NLTK, joblib, SciPy |
| Frontend | React 19, TypeScript, Vite, React Router, Axios |
| DevOps | Docker, Docker Compose, GitHub Actions |
| Testing | Pytest |

---

## Project Structure

```
QResolve/
│
├── app/
│   ├── api/                 # FastAPI routers (one file per resource)
│   │   ├── auth.py          # bootstrap / login / invitation accept / me
│   │   ├── organization.py
│   │   ├── user.py
│   │   ├── membership.py
│   │   ├── invitation.py
│   │   ├── department.py
│   │   ├── ticket.py        # create/list/update/assign/claim/resolve/predict/override
│   │   ├── comment.py
│   │   ├── audit.py
│   │   └── analytics.py
│   │
│   ├── core/                 # config, security, authorization, sessions, logging
│   ├── db/                   # SQLAlchemy engine/session setup
│   ├── models/                # ORM models (Organization, User, Membership, Ticket, ...)
│   ├── repositories/          # data-access layer, one repository per model
│   ├── services/              # business logic layer, one service per domain
│   ├── schemas/                # Pydantic request/response schemas
│   ├── predictor.py            # loads ML artifacts and runs priority prediction
│   ├── create_db.py
│   └── main.py                 # FastAPI app, router registration, middleware
│
├── alembic/                     # database migrations
├── artifacts/                   # trained model + vectorizer + encoders (.pkl)
│   ├── customer_satisfaction_model.pkl
│   ├── tfidf_vectorizer.pkl
│   ├── priority_encoder.pkl
│   └── metadata_feature_names.pkl
│
>>>>>>> feature/frontend-integration
├── data/                        # raw / processed datasets
├── processed/                   # cached train/test splits
├── notebook/                    # EDA -> validation -> feature engineering -> training -> evaluation -> inference
├── docs/
│   └── architecture/            # system, database, auth, authorization, API, and frontend design docs
├── frontend/                    # React + TypeScript SPA
│   └── src/
│       ├── pages/                # Login, Dashboard, Tickets
│       ├── components/            # shared UI + layout components
│       ├── services/               # API client (Axios) + ticket service
│       ├── hooks/, layouts/, routes/, styles/, types/
│       ├── pages/                # Login, Bootstrap, Dashboard, Tickets, Members, AuditLogs
│       ├── components/            # shared UI + layout components
│       ├── services/               # API client (Axios) + business services
│       ├── hooks/, routes/, styles/, types/
>>>>>>> feature/frontend-integration
├── src/                          # standalone data pipeline utilities (loader, validator, config)
├── tests/                        # pytest suite (API, auth/RBAC, services, repositories)
├── logs/
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
├── requirements.txt
└── .env.example
└── README.md
```

---

## Getting Started

### Prerequisites
- Python 3.11
- Node.js 18+ (for the frontend)
- Docker (optional, for containerized runs)

### Backend setup

```bash
git clone https://github.com/ADI-2707/QResolve.git
cd QResolve

python -m venv .venv

# Windows

.venv\Scripts\activate

.venv\Scripts\Activate.ps1

# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt

cp .env.example .env   # then edit values (SECRET_KEY especially)
```


Initialize the database (or use Alembic migrations — see below):

Initialize the database (or use Alembic migrations):


```bash
python -m app.create_db
```

Run the API:

```bash
uvicorn app.main:app --reload
```

- API: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

### Frontend setup

```bash
cd frontend
npm install
npm run dev
```

Other frontend scripts: `npm run build`, `npm run lint`, `npm run preview`.

---

## Configuration

Environment variables (`.env`, based on `.env.example`):

```env
API_TITLE="QResolve API"
API_DESCRIPTION="AI-powered Support Ticket Priority Prediction API"
API_VERSION=1.0.0

HOST=0.0.0.0
PORT=8000

LOG_LEVEL=INFO

DATABASE_URL=sqlite:///./qresolve.db

SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

To use PostgreSQL instead of SQLite, set `DATABASE_URL` to a Postgres DSN (e.g. `postgresql+psycopg2://user:password@host:5432/qresolve`) — the `psycopg2-binary` driver is already included in `requirements.txt`.

**Always change `SECRET_KEY`** before deploying anywhere beyond local development.

---

## API Overview

All resource endpoints are mounted under the `/api/v1` prefix (configurable via `API_V1_PREFIX`). The legacy top-level `/predict` and `/predictions` endpoints from the original single-tenant prototype are still present at the app root for backward compatibility.

| Router | Prefix | Endpoints |
|---|---|---|
| General | `/` | `GET /`, `GET /health` |
| Legacy prediction | `/` | `POST /predict`, `GET /predictions` |
| Auth | `/api/v1/auth` | `POST /bootstrap`, `POST /login`, `POST /invitations/accept`, `GET /me` |
| Organizations | `/api/v1/organizations` | `POST /`, `GET /`, `GET /{organization_id}`, `GET /slug/{slug}` |
| Users | `/api/v1/users` | `GET /{user_id}`, `GET /organization/{organization_id}`, `DELETE /{user_id}` |
| Memberships | `/api/v1/memberships` | `GET /`, `PATCH /{id}/role`, `POST /{id}/suspend`, `POST /{id}/activate` |
| Invitations | `/api/v1/invitations` | `POST /` |
| Departments | `/api/v1/departments` | `GET /`, `POST /`, `DELETE /{department_id}` |
| Tickets | `/api/v1/tickets` | `POST /`, `GET /`, `GET /{id}`, `PATCH /{id}`, `DELETE /{id}`, `PATCH /{id}/assign`, `POST /{id}/claim`, `POST /{id}/resolve`, `POST /{id}/predict`, `POST /{id}/predictions/{prediction_id}/override` |
| Comments | `/api/v1/tickets/{ticket_id}/comments` | `GET /`, `POST /` |
| Audit | `/api/v1/audit` | `GET /` |
| Analytics | `/api/v1/analytics` | `GET /tickets/overview` |

Full request/response contracts are documented in `docs/architecture/05_api_specification.md` and are also explorable live via `/docs`.

---

## Database & Migrations

The schema is defined with SQLAlchemy models under `app/models/`: `Organization`, `User`, `Membership`, `Department`, `Ticket`, `Comment`, `Invitation`, `AuditLog`, `Prediction`. Design rationale lives in `docs/architecture/02_database_design.md`.

Migrations are managed with Alembic:

```bash
alembic upgrade head                 # apply migrations
alembic revision --autogenerate -m "message"   # create a new migration
```

---

## Machine Learning Pipeline

The model artifacts in `artifacts/` (TF-IDF vectorizer, label/priority encoders, feature metadata, and the trained classifier) are loaded by `app/predictor.py` at runtime and used to predict ticket priority from ticket text plus metadata (`type`, `queue`, `tag_1`–`tag_4`).

The full modeling journey — EDA, dataset validation, feature engineering, training, evaluation, and building the inference pipeline — is documented step-by-step across the notebooks in `notebook/` (`01_eda.ipynb` through `11_inference_pipeline.ipynb`), along with two written reports in `docs/` (`dataset_investigation_report.md`, `baseline_experiment_report.md`).

---

## Testing
=======
Frontend will typically run at `http://127.0.0.1:5173`

Other frontend scripts: `npm run build`, `npm run lint`, `npm run preview`.

---

## Organization Bootstrap Flow

To create a new organization and set up the first admin account:

1. Navigate to the login page: `http://127.0.0.1:5173/login`
2. Click **"Create organization"** button
3. Fill in the bootstrap form:
   - Organization name
   - Admin first/last name
   - Admin email
   - Admin password
4. Click **"Create organization"**
5. You will be automatically logged in and redirected to the dashboard

---

## Configuration

Environment variables (`.env`, based on `.env.example`):

```env
API_TITLE="QResolve API"
API_DESCRIPTION="AI-powered Support Ticket Priority Prediction API"
API_VERSION=1.0.0

HOST=0.0.0.0
PORT=8000

LOG_LEVEL=INFO

DATABASE_URL=sqlite:///./qresolve.db

SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

To use PostgreSQL instead of SQLite, set `DATABASE_URL` to a Postgres DSN (e.g. `postgresql+psycopg2://user:password@host:5432/qresolve`) — the `psycopg2-binary` driver is already included in `requirements.txt`.

**Always change `SECRET_KEY`** before deploying anywhere beyond local development.

---

## API Overview

All resource endpoints are mounted under the `/api/v1` prefix. The legacy top-level `/predict` and `/predictions` endpoints from the original single-tenant prototype are still present at the app root for backward compatibility.

| Router | Prefix | Key Endpoints |
|---|---|---|
| Auth | `/api/v1/auth` | `POST /bootstrap`, `POST /login`, `POST /invitations/accept`, `GET /me` |
| Organizations | `/api/v1/organizations` | `POST /`, `GET /`, `GET /{organization_id}`, `GET /slug/{slug}` |
| Tickets | `/api/v1/tickets` | `POST /`, `GET /`, `GET /{id}`, `PATCH /{id}`, `POST /{id}/predict`, `POST /{id}/predictions/{prediction_id}/override` |
| Members | `/api/v1/memberships` | `GET /`, `PATCH /{id}/role`, `POST /{id}/suspend`, `POST /{id}/activate` |
| Invitations | `/api/v1/invitations` | `POST /` |
| Audit | `/api/v1/audit` | `GET /` |
| Analytics | `/api/v1/analytics` | `GET /tickets/overview` |

Full request/response contracts are documented in the interactive API docs (`/docs`).

---

## Running Tests

```bash
python -m pytest -v
```


The suite (`tests/`) covers the API surface, auth/RBAC, ticket prediction service, ticket repository, membership administration, comments, departments, audit logging, analytics, and API versioning.

---

## Docker

```bash
docker build -t qresolve-api .
=======
---

## Docker

Build and run with Docker Compose:

```bash
docker-compose up --build
```

---

## License

MIT

---

## Contributing

Contributions welcome! Please submit a pull request with a clear description of your changes.

```bash
docker run -p 8000:8000 qresolve-api
```

Or with Compose (includes a `/health` healthcheck):

```bash
docker compose up --build
docker compose down
```

---

## Logging

The application logs:
- API startup/shutdown
- Every incoming request (method, path, status, duration)
- Prediction requests and results
- Database operations
- Exceptions (validation errors and unhandled exceptions have dedicated handlers)

Logs are written to `logs/`.

---

## Architecture Docs

For a deeper dive beyond this README, see [`docs/architecture/`](docs/architecture):

- `01_system_architecture.md` — overall system design and principles
- `02_database_design.md` — schema and data model rationale
- `03_authentication_design.md` — auth flow details
- `04_authorization_matrix.md` — role → permission matrix
- `05_api_specification.md` — full API contract
- `06_frontend_architecture.md` — frontend structure and conventions
- `legacy_architecture.md` — the original single-tenant design this project evolved from

---

## License

MIT License.

## Author

**Aditya Singh**
GitHub: [github.com/ADI-2707](https://github.com/ADI-2707)
