# DockrBoard (Docker practice project)

Phase 1: base Docker setup

# DockrBoard — Phase 1: Project Structure & Base Docker Setup

**Objective:**  
Set up the foundational structure of the project with Docker containers for backend, frontend, database, and Redis. This phase ensures a working development environment without adding business logic yet.

---

## 1. Project Skeleton

- Main project folder: `dockrboard`  
- Two directories: `backend` (Django) and `frontend` (Next.js/React)  

---

## 2. Top-Level Files

Files in the project root:

- `docker-compose.yml` – orchestrates containers.  
- `.env` – environment variables for Django, PostgreSQL, frontend.  
- `.gitignore` – ignores Python, Node, Docker, editor artifacts.  
- `.dockerignore` – excludes unnecessary files from Docker /images.  
- `README.md` – project documentation (this file).  

---

## 3. Backend Skeleton

- Minimal Django project inside `backend/`  
- Main Django project: `config/`  
- Optional `app/` folder for future apps  
- Dockerfile installs Python, dependencies, and runs Gunicorn  
- Requirements include Django, Gunicorn, DRF, Channels, Redis, tenants, OAuth toolkit  
- Minimal settings allow startup, DB connection, and static files serving  

---

## 4. Frontend Skeleton

- Minimal Next.js project inside `frontend/`  
- Dockerfile installs Node and runs dev server  
- Homepage displays a simple message and backend API URL  
- Core dependencies: React, Next.js, Tailwind CSS, Alpine.js  

---

## 5. Docker Setup

**Services included:**

- **web**: Django backend (Gunicorn)  
- **frontend**: Next.js dev server  
- **db**: PostgreSQL  
- **redis**: caching/message broker  

**Volumes:** Persist database data outside containers.  

**Dependencies:** `web` depends on `db` and `redis`; `frontend` depends on `web`.  

---

## 6. Running the Project

## Containers, Images, and Volumes

Docker manages the project using **containers**, **images**, and **volumes**. Here's what happens in Phase 1:

---

### Build and start all containers

```bash
docker compose up -d --build
```

## Process:

#### **Builds Docker images** for each service (web, frontend, db, redis) from their Dockerfiles.

![Images](/images/phase_1/images.png)
#### **Creates containers:** from these images:

![Containers](/images/phase_1/containers.png)

**Containers**
- **dockrboard_web** (Django backend)
- **dockrboard_frontend** (Next.js)
- **dockrboard_db** (Postgres)
- **dockrboard_redis** (Redis)

#### **Creates a named volume** ```postgres_data``` to persist database data outside the container.

When **volumes** are deleted

Default behavior:
```bash
docker compose down
```

- This stops and removes containers, but volumes are preserved by default. This prevents accidental data loss.

**Delete** volumes explicitly:
```bash
docker compose down --volumes
```

![Volumes](/images/phase_1/volumes.png)

- This removes the named volumes along with the containers, including all stored data (e.g., your database contents).

## Docker Screenshots — Phase 1

**1. Docker Up**  
Command:
```bash
docker compose up -d --build
```

![Docker Up](/images/phase_1/dkr_up.png)

**2. Running Containers**
Command:
```bash
docker compose ps
docker  ps
```

![Running Containers](/images/phase_1/rng_cont.png)

**3. Logs**
Command:
```bash
docker compose logs -f web
```

![Docker Logs](/images/phase_1/web_log.png)

**4. Docker Down**
Command:
```bash
docker compose down --volumes
```

![Docker Logs](/images/phase_1/down.png)

**5. Rebuild Web Service**
Command:
```bash
docker compose build -d web
```

![Rebuild Web](/images/phase_1/down_to_up.png)

**6. Stop Containers**
Command:
```bash
docker compose stop web
```

![Stop Web](/images/phase_1/stp.png)