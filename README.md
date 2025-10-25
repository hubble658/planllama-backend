PlanLLaMA Backend API

A Flask-based REST API backend for the PlanLLaMA project management application, utilizing PostgreSQL (or SQLite for development) and SQLAlchemy.

Features

  - Core API: RESTful endpoints for Projects, Tasks, and Employees.
  - Data Layer: PostgreSQL with SQLAlchemy ORM and Flask-Migrate for database migrations.
  - Integration: CORS support for seamless frontend connection.
  - Analytics: Endpoints for project statistics and employee workload.
  - Advanced: Full CRUD operations with filtering and querying capabilities.

-----

Tech Stack

  - Python 3.8+
  - Flask (Web framework)
  - SQLAlchemy (ORM)
  - PostgreSQL (Database - SQLite for development)
  - Flask-Migrate (Database migrations)
  - Flask-CORS (Cross-origin resource sharing)

-----

Installation & Setup

Prerequisites

  - Python 3.8 or higher
  - PostgreSQL (or use SQLite for development)

Steps

1.  Clone & Navigate
    git clone \<repository-url\>
    cd backend

2.  Create Virtual Environment
    python -m venv venv
    source venv/bin/activate  \# macOS/Linux

# venv\\Scripts\\activate   \# Windows

3.  Install Dependencies
    pip install -r requirements.txt

4.  Configure Environment
    Copy the example file and edit it with your settings:
    cp .env.example .env

Example .env configuration:
FLASK\_ENV=development
SECRET\_KEY=your-secret-key-here

# For PostgreSQL

DATABASE\_URL=postgresql://username:password@localhost:5432/planllama

# OR for SQLite (development)

# DATABASE\_URL=sqlite:///planllama.db

CORS\_ORIGINS=http://localhost:5173,http://localhost:3000

5.  Initialize Database
    For development, use the script to set up tables.

# Create tables only

python init\_db.py

# Create tables and seed with sample data

python init\_db.py --seed

6.  Run Application
    python app.py
    The API will be available at http://localhost:5000.

-----

Production Setup (Flask-Migrate)
For robust database management in production, use Flask-Migrate:

Command | Description
flask db init | Initialize migrations (first time only)
flask db migrate -m "..." | Create a new migration script after model changes
flask db upgrade | Apply all pending migrations to the database
python -c "from app import app; from seed import seed\_database; app.app\_context().push(); seed\_database()" | Seed the database (if needed)

-----

API Endpoints Reference

Employees
Method | Endpoint | Description
GET | /api/employees | Get all employees (or filter by ?role=pm/executor)
GET | /api/employees/\<id\> | Get specific employee
POST/PUT/DELETE | /api/employees[/\<id\>] | CRUD operations
GET | /api/employees/\<id\>/workload | Get employee workload statistics

Projects
Method | Endpoint | Description
GET | /api/projects | Get all projects (Filter by ?status= or ?include\_tasks=true)
GET | /api/projects/\<id\> | Get specific project
POST/PUT/DELETE | /api/projects[/\<id\>] | CRUD operations
GET | /api/projects/\<id\>/tasks | Get all tasks for a project
GET | /api/projects/\<id\>/stats | Get project statistics

Tasks
Method | Endpoint | Description
GET | /api/tasks | Get all tasks (Filter by ?status=, ?assignee\_id=, ?project\_id=)
GET | /api/tasks?enrich=true | Get tasks with assignee and project names
GET | /api/tasks/\<id\> | Get specific task
POST/PUT/DELETE | /api/tasks[/\<id\>] | CRUD operations
PATCH | /api/tasks/\<id\>/status | Update task status only
GET | /api/tasks/stats | Get global task statistics

-----

Data Models
The API uses the following core models:

Employee
Field | Type | Description
employee\_id (PK) | String | Unique identifier
user\_role | String | Role type: pm or executor
capacity\_hours\_per\_week | Int | Max working hours
current\_load\_hours | Int | Calculated assigned hours
skills | JSON | List of skills and levels

Project
Field | Type | Description
project\_id (PK) | String | Unique identifier
status | String | Planning, In Progress, On Hold, Completed
priority | String | low, medium, high, critical
tasksCount | Int | Total number of tasks (included in response)
completedTasks | Int | Number of completed tasks (included in response)

Task
Field | Type | Description
task\_id (PK) | String | Unique identifier
assignee\_id (FK) | String | Links to employees.employee\_id
project\_id (FK) | String | Links to projects.project\_id
estimatedHours | Int | Estimated effort
status | String | Pending, In Progress, Completed, Blocked
assignee / project | String | Name (only when enrich=true)

-----

API Usage Examples

Update Task Status
Use a PATCH request for partial updates.
curl -X PATCH http://localhost:5000/api/tasks/t01/status -H "Content-Type: application/json" -d '{"status": "Completed"}'

Get Enriched Tasks
Retrieve tasks including the names of the assignee and project.
curl http://localhost:5000/api/tasks?enrich=true

Create a New Project
curl -X POST http://localhost:5000/api/projects -H "Content-Type: application/json" -d '{"project\_id": "p06", "name": "New Project", "status": "Planning", "dueDate": "2025-12-31", "priority": "high"}'

-----

Development & Testing

Development Mode
Run the app with Flask development settings enabled:
export FLASK\_ENV=development
python app.py

Running Tests
Assuming tests are set up with unittest (see test\_api.py):
python test\_api.py

Troubleshooting

  - Database Connection: Verify PostgreSQL is running and DATABASE\_URL in .env is correct.
  - CORS Errors: Ensure the frontend origin (http://localhost:5173, etc.) is listed in the CORS\_ORIGINS variable in .env.

-----

Deployment (Production)

Gunicorn Setup
For production, use a WSGI server like Gunicorn:
pip install gunicorn

# Run with 4 worker processes

gunicorn -w 4 -b 0.0.0.0:5000 app:app

Docker Deployment
The repository includes a Dockerfile for easy containerization:
docker build -t planllama-backend .
docker run -p 5000:5000 planllama-backend

-----

License
This project is licensed under the MIT License.

-----