# Saftehnika - Vue + Django Application

A full-stack application with Vue.js frontend and Django REST API backend, fully containerized with Docker.

## Architecture

- **Frontend**: Vue.js application served by Nginx
- **API**: Django REST Framework with PostgreSQL database
- **Database**: PostgreSQL 15

## Prerequisites

- Docker (20.10+)
- Docker Compose (2.0+)

## Quick Start

### 1. Clone and Setup

```bash
# Clone the repository (if not already done)
git clone <your-repo-url>
cd saftehnika

# Copy environment file
cp .env.example .env
```

### 2. Configure Environment

Edit `.env` file and update the following:
- `SECRET_KEY`: Generate a secure random key for Django
- `POSTGRES_PASSWORD`: Set a strong password for production
- `DEBUG`: Set to `0` for production, `1` for development

### 3. Build and Run

```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build
```

The application will be available at:
- **Frontend**: http://localhost:3002
- **API**: http://localhost:8000
- **API Admin**: http://localhost:8000/admin

### 4. Create Django Superuser (First Time)

```bash
docker-compose exec api python manage.py createsuperuser
```

## Development

### Running in Development Mode

1. Set `DEBUG=1` in `.env` file
2. Rebuild and restart:
   ```bash
   docker-compose down
   docker-compose up --build
   ```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api
docker-compose logs -f frontend
docker-compose logs -f db
```

### Execute Commands in Containers

```bash
# Django management commands
docker-compose exec api python manage.py <command>

# Install new Python package
docker-compose exec api pip install <package>
# Then add to requirements.txt and rebuild

# Install new npm package
docker-compose exec frontend npm install <package>
# Then rebuild the frontend
```

### Database Management

```bash
# Run migrations
docker-compose exec api python manage.py migrate

# Create new migration
docker-compose exec api python manage.py makemigrations

# Access PostgreSQL shell
docker-compose exec db psql -U saftehnika_user -d saftehnika

# Backup database
docker-compose exec db pg_dump -U saftehnika_user saftehnika > backup.sql

# Restore database
docker-compose exec -T db psql -U saftehnika_user -d saftehnika < backup.sql
```

## Stopping the Application

```bash
# Stop services (preserves volumes)
docker-compose down

# Stop and remove volumes (data will be lost)
docker-compose down -v
```

## Project Structure

```
saftehnika/
├── docker-compose.yml          # Container orchestration
├── .env.example                # Environment variables template
├── .env                        # Environment variables (create from .env.example)
├── vue/                        # Frontend application
│   ├── Dockerfile              # Vue app container configuration
│   ├── nginx.conf              # Nginx configuration
│   ├── .dockerignore           # Docker ignore patterns
│   └── ...                     # Vue source files
└── django/                     # Backend API
    ├── Dockerfile              # Django container configuration
    ├── .dockerignore           # Docker ignore patterns
    ├── requirements.txt        # Python dependencies
    └── ...                     # Django source files
```

## Troubleshooting

### Port Already in Use

If you get port conflict errors:
```bash
# Change ports in docker-compose.yml
# For frontend: "8080:80" instead of "80:80"
# For API: "8001:8000" instead of "8000:8000"
```

### Database Connection Issues

```bash
# Check database health
docker-compose ps

# Restart database service
docker-compose restart db

# View database logs
docker-compose logs db
```

### Rebuild After Code Changes

```bash
# Rebuild specific service
docker-compose up -d --build api
docker-compose up -d --build frontend

# Rebuild all services
docker-compose up -d --build
```

### Container Won't Start

```bash
# Check container status
docker-compose ps

# View detailed logs
docker-compose logs --tail=100 api

# Access container shell for debugging
docker-compose exec api sh
```

## Production Deployment

For production deployment:

1. **Update `.env`**:
   - Generate secure `SECRET_KEY`
   - Set `DEBUG=0`
   - Update `ALLOWED_HOSTS` with your domain
   - Set strong database password
   - Update `CORS_ALLOWED_ORIGINS`

2. **Use production compose file**:
   ```bash
   docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
   ```

3. **Setup SSL/TLS**: Configure reverse proxy (nginx/traefik) with Let's Encrypt

4. **Setup monitoring**: Add health checks and logging infrastructure

5. **Backup strategy**: Implement regular database backups

## Additional Commands

```bash
# Remove all stopped containers
docker-compose rm

# View resource usage
docker stats

# Clean up Docker system
docker system prune -a
```
