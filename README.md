# Saftehnika — setup from scratch

## Prerequisites

- **Docker** and **Docker Compose**, or **Python 3.11+**, **Node.js 20+**, and **PostgreSQL 15+**.

---

## Docker Compose

1. Clone the repository and open the project root.

2. Create an environment file:

   ```bash
   cp .env.example .env
   ```

   Ensure `API_URL` points at the API the browser will use (Compose exposes the API on port `8000`):

   ```env
   API_URL=http://localhost:8000/api
   ```

3. Build and start services:

   ```bash
   docker compose build
   docker compose up -d
   ```

   The API container runs migrations on startup. To run them manually:

   ```bash
   docker compose exec api python manage.py migrate --noinput
   ```

4. Load fixture data from `django/data/` in this order:

   ```bash
   docker compose exec api python manage.py import_sensor_types
   docker compose exec api python manage.py import_metrics
   docker compose exec api python manage.py import_sensors
   ```

5. **Django admin** — create a superuser (interactive prompts for username, email, password), then open [http://localhost:8000/admin/](http://localhost:8000/admin/) in the browser:

   ```bash
   docker compose exec api python manage.py createsuperuser
   ```

6. **Frontend** — open [http://localhost:3002](http://localhost:3002/) in the browser.