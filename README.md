# QResolve

> AI-powered Support Ticket Priority Prediction Platform built with Machine Learning, FastAPI, SQLAlchemy, Docker, and SQLite.

---

# Overview

QResolve is an end-to-end Machine Learning project that predicts the priority of customer support tickets using Natural Language Processing (NLP) and Machine Learning.

The application exposes a REST API using FastAPI and stores prediction history in a relational database using SQLAlchemy.

The project demonstrates a complete production-ready ML workflow including:

- Data validation
- Feature engineering
- Model training
- Model serialization
- REST API
- Database integration
- Docker containerization
- Unit testing
- Logging
- Exception handling

---

# Features

- Predict ticket priority using a trained ML model
- Store prediction history automatically
- Retrieve previous predictions
- FastAPI interactive documentation
- SQLite database integration using SQLAlchemy
- Docker support
- Structured logging
- Custom exception handling
- Unit tests with Pytest
- Environment variable configuration

---

# Tech Stack

## Programming

- Python 3.11

## Machine Learning

- Pandas
- NumPy
- Scikit-learn
- Joblib

## Backend

- FastAPI
- Uvicorn
- Pydantic

## Database

- SQLAlchemy
- SQLite

## DevOps

- Docker
- Docker Compose

## Testing

- Pytest

## Development

- Git
- GitHub
- PyCharm

---

# Project Structure

```text
QResolve/
│
├── app/
│   ├── config.py
│   ├── create_db.py
│   ├── database.py
│   ├── exceptions.py
│   ├── logger.py
│   ├── main.py
│   ├── models.py
│   ├── predictor.py
│   └── schemas.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── docs/
│
├── logs/
│
├── models/
│   ├── random_forest.pkl
│   ├── tfidf_vectorizer.pkl
│   ├── label_encoder.pkl
│   └── ...
│
├── notebook/
│
├── src/
│   ├── data_loader.py
│   ├── data_validator.py
│   ├── feature_engineering.py
│   ├── logger.py
│   └── utils.py
│
├── tests/
│   ├── test_api.py
│   ├── test_database.py
│   ├── test_data_loader.py
│   └── test_data_validator.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Installation

## Clone repository

```bash
git clone https://github.com/ADI-2707/QResolve.git
```

Move into the project

```bash
cd QResolve
```

Create virtual environment

```bash
python -m venv .venv
```

Activate environment

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Running the API

Start the FastAPI server

```bash
uvicorn app.main:app --reload
```

API will be available at

```
http://127.0.0.1:8000
```

Swagger UI

```
http://127.0.0.1:8000/docs
```

ReDoc

```
http://127.0.0.1:8000/redoc
```

---

# API Endpoints

## GET /

Returns API information.

---

## GET /health

Returns API health status.

Example response

```json
{
  "status": "healthy"
}
```

---

## POST /predict

Predicts ticket priority.

Example request

```json
{
  "text": "Customer cannot login after password reset.",
  "type": "Technical issue",
  "queue": "Support",
  "tag_1": "Authentication",
  "tag_2": "Login",
  "tag_3": "Password Reset",
  "tag_4": "Account"
}
```

Example response

```json
{
  "priority": "Medium"
}
```

---

## GET /predictions

Returns prediction history stored in the database.

---

# Database

QResolve uses SQLAlchemy ORM with SQLite.

Prediction requests are automatically stored in the database.

Current table:

- predictions

---

# Running Tests

Execute all tests

```bash
python -m pytest -v
```

Current status

```
23 tests passed
```

---

# Docker

Build Docker image

```bash
docker build -t qresolve-api .
```

Run container

```bash
docker run -p 8000:8000 qresolve-api
```

Using Docker Compose

```bash
docker compose up --build
```

Stop services

```bash
docker compose down
```

---

# Configuration

Application settings are managed using environment variables.

Example `.env`

```env
API_TITLE=QResolve API
API_VERSION=1.0.0
HOST=0.0.0.0
PORT=8000

DATABASE_URL=sqlite:///./database/qresolve.db

LOG_LEVEL=INFO
```

---

# Logging

The application logs

- API startup
- Incoming requests
- Prediction requests
- Database operations
- Exceptions

---

# Future Improvements

- PostgreSQL support
- Alembic database migrations
- User authentication
- Role-based authorization
- CI/CD with GitHub Actions
- Cloud deployment
- Model monitoring
- API rate limiting
- Request caching

---

# Version Control

This project follows the Conventional Commits specification.

Examples

```text
feat(api): add prediction history endpoint

fix(database): resolve SQLite initialization issue

refactor(api): simplify prediction workflow

docs: update README

test(api): add prediction endpoint tests

build(docker): optimize Docker image
```

---

# License

This project is licensed under the MIT License.

---

# Author

**Aditya Singh**

GitHub: https://github.com/ADI-2707