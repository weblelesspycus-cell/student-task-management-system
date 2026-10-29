# Student Task Management System (Docker)

A responsive Flask web application for managing academic tasks. Features include adding tasks, descriptions, due dates, priority, status updates, search, status filtering, summary counts, and deletion.

## Requirements

- Docker Desktop (Windows/macOS) or Docker Engine + Docker Compose plugin (Linux)
- A modern web browser
- Internet access for the initial image build (to download Python packages)

You do not need to install Python locally if you use Docker.

## Run with Docker Compose (recommended)

1. Install and start Docker Desktop, or make sure Docker Engine is running.
2. Extract this project folder.
3. Open a terminal in the `student_task_manager` folder.
4. Build and start the application:

   ```bash
   docker compose up --build -d
   ```

5. Open **http://localhost:5000** in your browser.

## Useful commands

```bash
# Show running containers
docker compose ps

# View application logs
docker compose logs -f

# Stop the application (keeps saved data)
docker compose down

# Start it again
docker compose up -d

# Stop and delete the database volume too (DELETES SAVED TASKS)
docker compose down -v

# Build a named image manually
docker build -t student-task-manager:1.0 .

# Run the image without Compose (uses a named volume for persistent data)
docker volume create student-task-data
docker run -d --name student-task-manager-manual \
  -p 5000:5000 \
  -e DATABASE_PATH=/data/tasks.db \
  -v student-task-data:/data \
  student-task-manager:1.0

# Stop and remove the manually created container
docker stop student-task-manager-manual
docker rm student-task-manager-manual
```

If port 5000 is already in use, change the left side of the port mapping in `compose.yaml` from `5000:5000` to `8080:5000`, restart with `docker compose up -d`, and visit **http://localhost:8080**.

## Test checklist

1. Open the app and confirm the dashboard loads.
2. Add a task with a title, description, due date and High priority.
3. Add another task with a different priority.
4. Change one task from Pending to In Progress, then Completed.
5. Search for a word from a task title or description.
6. Filter by each status.
7. Delete a task and confirm it disappears.
8. Run `docker compose down`, then `docker compose up -d`; verify remaining tasks still exist. This checks the named volume.
9. Run `docker compose ps` and `docker compose logs --tail=50` to collect deployment evidence.

## Project structure

```text
student_task_manager/
├── app.py
├── requirements.txt
├── Dockerfile
├── compose.yaml
├── .dockerignore
├── .env.example
├── README.md
├── templates/
│   ├── base.html
│   ├── index.html
│   └── error.html
└── static/
    └── style.css
```

## How Docker is used

- `Dockerfile` defines the image: Python base image, dependencies, application files, unprivileged user, exposed port and startup command.
- `compose.yaml` builds and starts the service, publishes host port 5000 to container port 5000, and attaches a named volume called `task_data`.
- The application listens on `0.0.0.0:5000` inside the container so Docker can route requests to it.
- SQLite stores tasks at `/data/tasks.db`. The named volume preserves the database when the container is removed or recreated.
- Gunicorn runs the Flask application as the production-style WSGI server rather than Flask's development server.

## Limitations and production notes

This is an educational prototype for local demonstration. It does not include user accounts, authentication, multi-user permissions, CSRF protection or automated backups. Do not expose it publicly with real or sensitive data without adding these controls, secure secrets, HTTPS, monitoring and a backup plan.
