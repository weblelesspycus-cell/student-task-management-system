# Assignment Report: Student Task Management System Hosted Using Docker

## 1. Title
**Design and Deployment of a Student Task Management System Using Docker**

## 2. Introduction
Students often manage assignments, presentations, projects and deadlines across different notes and applications. This can make it difficult to track priorities and completion status. The Student Task Management System is a web-based application designed to keep academic tasks in one place. The application is packaged and run in a Docker container to make deployment more consistent and reproducible.

## 3. Aim and Objectives
**Aim:** To develop and deploy a web-based Student Task Management System using Docker.

**Objectives:**
1. Develop a responsive web interface for managing academic tasks.
2. Allow users to create, search, filter, update and delete tasks.
3. Store task information in an SQLite database.
4. Package the application and its dependencies into a Docker image.
5. Run the application in a Docker container and preserve its database using a named volume.
6. Test the major features and verify that the deployed application is accessible through a browser.

## 4. Scope and Features
The prototype supports:
- Creating tasks with a title, description, due date, priority and status.
- Viewing tasks and summary counts.
- Updating task status to Pending, In Progress or Completed.
- Searching tasks by title or description.
- Filtering tasks by status.
- Deleting tasks.
- Highlighting overdue tasks.
- Persistent SQLite storage through a Docker named volume.

User registration, authentication, multiple-user permissions, notifications and cloud-scale deployment are outside the current scope.

## 5. Technologies Used
- **Python:** Main programming language.
- **Flask:** Web framework for routes and request handling.
- **HTML:** Page structure.
- **CSS:** Responsive presentation and styling.
- **SQLite:** Relational database for task records.
- **Gunicorn:** WSGI server used to serve the Flask application in the container.
- **Docker:** Packages the application and its runtime dependencies into an image.
- **Docker Compose:** Defines the service, port mapping, environment variables and persistent volume.

## 6. System Design
A user opens the application in a web browser at `http://localhost:5000`. The browser sends HTTP requests to the Flask application running inside the Docker container. Flask validates inputs and performs database operations through SQLite. The database file is stored at `/data/tasks.db`, which is backed by a Docker named volume. This keeps task data separate from the container's writable layer and allows it to survive container replacement.

### Architecture
Browser → Published Docker port → Gunicorn/Flask application → SQLite database in named volume.

## 7. Docker Implementation
The `Dockerfile` starts from a lightweight Python image, installs the dependencies listed in `requirements.txt`, copies the application code, creates a non-root user, and starts Gunicorn on port 5000.

The `compose.yaml` file:
- Builds the image from the project directory.
- Publishes port `5000` on the host to port `5000` in the container.
- Sets the database path to `/data/tasks.db`.
- Mounts the named volume `task_data` at `/data`.
- Configures the container to restart unless it is explicitly stopped.

The application binds to `0.0.0.0` inside the container so Docker's published port can reach it.

## 8. Deployment Procedure
1. Install and start Docker Desktop, or Docker Engine and the Docker Compose plugin on Linux.
2. Extract the project ZIP file.
3. Open a terminal in the `student_task_manager` folder.
4. Run `docker compose up --build -d`.
5. Confirm the service is running with `docker compose ps`.
6. Open `http://localhost:5000` in a browser.
7. Test task creation, searching, filtering, status changes and deletion.
8. Run `docker compose down`, then `docker compose up -d`, and confirm saved tasks remain.

## 9. Testing Plan and Results Record
Complete the following tests after deployment and record the actual result. Do not claim a test passed until you have performed it.

| Test | Procedure | Expected result | Actual result |
|---|---|---|---|
| Application access | Open `http://localhost:5000` | Dashboard loads | To be completed |
| Create task | Submit a task with a title | Task appears in the list and total increases | To be completed |
| Required title | Submit the form with no title | Validation message appears | To be completed |
| Update status | Change a task to Completed | Status and summary count update | To be completed |
| Search | Search for a unique task word | Matching task(s) appear | To be completed |
| Filter | Select Pending or Completed | Only tasks with selected status appear | To be completed |
| Delete task | Delete a task and confirm | Task is removed | To be completed |
| Persistence | Stop and restart the Compose service | Previously saved tasks remain | To be completed |

Useful evidence commands:
- `docker compose ps`
- `docker compose logs --tail=50`
- `docker image ls`

Take screenshots of the working dashboard, a created task, an updated status, the running container and the successful persistence test for the final submission if required.

## 10. Benefits
- Centralizes academic tasks and deadlines.
- Makes priorities and progress easy to review.
- Provides a browser-based interface without installing the application on every user's machine.
- Docker makes the application environment reproducible.
- A named volume protects task data from normal container recreation.

## 11. Limitations and Future Improvements
The prototype does not provide authentication, user-specific task lists, CSRF protection, automated backups, reminders or a public HTTPS endpoint. Future versions could add user accounts, role-based access, notifications, a stronger database for multi-user deployment, automated tests, HTTPS, backups and deployment to a cloud host.

## 12. Conclusion
The project demonstrates a complete small web application packaged and run using Docker. Flask provides the application logic, SQLite stores tasks, Gunicorn serves the application, and Docker Compose manages the container and persistent data volume. Once the deployment and test checklist has been completed, the student can demonstrate both the application's functionality and the use of containerization.

## 13. References
- Docker documentation: https://docs.docker.com/
- Docker Compose documentation: https://docs.docker.com/compose/
- Flask documentation: https://flask.palletsprojects.com/
- Python documentation: https://docs.python.org/3/
- SQLite documentation: https://www.sqlite.org/docs.html
