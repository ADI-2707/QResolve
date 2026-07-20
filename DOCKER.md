# Docker Setup for QResolve

This guide explains how to run QResolve using Docker and Docker Compose.

## Prerequisites

- Docker (version 20.10+)
- Docker Compose (version 2.0+)

## Quick Start

### Build and Run Everything

```bash
docker-compose up --build
```

This will:
- Build the backend Docker image (Python FastAPI)
- Build the frontend Docker image (Node.js React Vite)
- Start both services on a shared Docker network
- Initialize the database automatically

### Access the Application

Once all services are running:

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Service Details

### Backend Service (`qresolve-api`)

- **Image**: Built from `Dockerfile` (Python 3.11)
- **Port**: 8000
- **Container**: `qresolve-api`
- **Environment**:
  - `DATABASE_URL=sqlite:///./qresolve.db`
  - `SECRET_KEY` (change in production)
  - `LOG_LEVEL=INFO`
  - `HOST=0.0.0.0`
  - `PORT=8000`

**Health Check**: Pings `/health` endpoint every 30 seconds

### Frontend Service (`qresolve-frontend`)

- **Image**: Built from `frontend/Dockerfile` (Node.js 18 Alpine)
- **Port**: 5173
- **Container**: `qresolve-frontend`
- **Built with**: Vite + React + TypeScript
- **Served by**: Node serve package
- **Environment**:
  - `VITE_API_URL=http://qresolve-api:8000/api/v1` (Docker network URL)

## Docker Network

Both services communicate via the `qresolve-network` bridge network:

- Backend is accessible to frontend as `http://qresolve-api:8000`
- Frontend is accessible as `http://qresolve-frontend:5173`

## Managing Containers

### Start Services

```bash
docker-compose up
```

### Run in Background

```bash
docker-compose up -d
```

### Stop Services

```bash
docker-compose down
```

### Stop and Remove Volumes

```bash
docker-compose down -v
```

### View Logs

```bash
docker-compose logs -f
```

Backend logs:
```bash
docker-compose logs -f qresolve-api
```

Frontend logs:
```bash
docker-compose logs -f qresolve-frontend
```

### Rebuild Images

```bash
docker-compose up --build
```

## Environment Configuration

### Production Setup

Create a `.env.production` file for production secrets:

```env
SECRET_KEY=your-very-secure-secret-key-here
DATABASE_URL=postgresql+psycopg2://user:password@db-host:5432/qresolve
LOG_LEVEL=WARNING
```

Update `docker-compose.yml` to use `.env.production`:

```yaml
services:
  qresolve-api:
    env_file: .env.production
```

### PostgreSQL Integration (Optional)

To use PostgreSQL instead of SQLite, add a database service to `docker-compose.yml`:

```yaml
services:
  postgres:
    image: postgres:15-alpine
    container_name: qresolve-db
    environment:
      POSTGRES_DB: qresolve
      POSTGRES_USER: qresolve
      POSTGRES_PASSWORD: your-password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - qresolve-network

  qresolve-api:
    # ... existing config ...
    environment:
      - DATABASE_URL=postgresql+psycopg2://qresolve:your-password@postgres:5432/qresolve
      # ... rest of env ...
    depends_on:
      - postgres

volumes:
  postgres_data:
```

## Troubleshooting

### Frontend Cannot Connect to Backend

Check that the `VITE_API_URL` environment variable is set correctly in the frontend service.

For Docker: `http://qresolve-api:8000/api/v1`
For local dev: `http://localhost:8000/api/v1`

### Database Not Initializing

The backend automatically runs `python -m app.create_db` during image build. If needed manually:

```bash
docker-compose exec qresolve-api python -m app.create_db
```

### Port Conflicts

If ports 5173 or 8000 are already in use, update `docker-compose.yml`:

```yaml
services:
  qresolve-api:
    ports:
      - "9000:8000"  # Maps host 9000 to container 8000
  
  qresolve-frontend:
    ports:
      - "5174:5173"  # Maps host 5174 to container 5173
```

### Clearing Build Cache

```bash
docker-compose down -v
docker system prune -a
docker-compose up --build
```

## Production Deployment

### Using a Production Server

Replace `serve` in `frontend/Dockerfile` with nginx for better performance:

```dockerfile
# Production stage
FROM nginx:alpine

COPY --from=builder /app/frontend/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
```

### Environment Variables

Always set these for production:

```env
SECRET_KEY=<generate-a-secure-random-key>
ENVIRONMENT=production
LOG_LEVEL=WARNING
DATABASE_URL=<production-database-url>
```

### Scale with Replicas

```yaml
services:
  qresolve-api:
    deploy:
      replicas: 3
```

## Files

- `Dockerfile` - Backend image definition
- `frontend/Dockerfile` - Frontend image definition
- `docker-compose.yml` - Multi-container orchestration
- `.dockerignore` - Files/folders to exclude from Docker builds
