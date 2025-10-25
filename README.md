# PlanLLaMA Backend API

A Flask-based REST API backend for the PlanLLaMA project management application, using PostgreSQL and SQLAlchemy.

## Features

- 🚀 RESTful API endpoints for Projects, Tasks, and Employees
- 🗄️ PostgreSQL database with SQLAlchemy ORM
- 🔄 Database migrations with Flask-Migrate
- 🌐 CORS support for frontend integration
- 📊 Comprehensive data models with relationships
- 🎯 Full CRUD operations for all entities
- 📈 Statistics and analytics endpoints
- 🔍 Advanced filtering and querying

## Tech Stack

- **Python 3.8+**
- **Flask** - Web framework
- **SQLAlchemy** - ORM
- **PostgreSQL** - Database (SQLite for development)
- **Flask-Migrate** - Database migrations
- **Flask-CORS** - Cross-origin resource sharing

## Prerequisites

- Python 3.8 or higher
- PostgreSQL (or use SQLite for development)
- pip (Python package manager)

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd backend
```

### 2. Create virtual environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and configure your settings:

```env
# For PostgreSQL
DATABASE_URL=postgresql://username:password@localhost:5432/planllama

# For SQLite (development)
DATABASE_URL=sqlite:///planllama.db

FLASK_ENV=development
SECRET_KEY=your-secret-key-here
```

### 5. Initialize the database

```bash
# Create tables only
python init_db.py

# Create tables and seed with sample data
python init_db.py --seed
```

### 6. Run the application

```bash
python app.py
```

The API will be available at `http://localhost:5000`

## Alternative: Using Flask-Migrate

For production, use Flask-Migrate for better database management:

```bash
# Initialize migrations (first time only)
flask db init

# Create a migration
flask db migrate -m "Initial migration"

# Apply migrations
flask db upgrade

# Seed the database
python -c "from app import app; from seed import seed_database; app.app_context().push(); seed_database()"
```

## API Endpoints

### Employees

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/employees` | Get all employees |
| GET | `/api/employees?role=pm` | Get employees by role (pm/executor) |
| GET | `/api/employees/<employee_id>` | Get specific employee |
| POST | `/api/employees` | Create new employee |
| PUT | `/api/employees/<employee_id>` | Update employee |
| DELETE | `/api/employees/<employee_id>` | Delete employee |
| GET | `/api/employees/<employee_id>/workload` | Get employee workload stats |

### Projects

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/projects` | Get all projects |
| GET | `/api/projects?status=In Progress` | Filter projects by status |
| GET | `/api/projects?include_tasks=true` | Get projects with tasks |
| GET | `/api/projects/<project_id>` | Get specific project |
| POST | `/api/projects` | Create new project |
| PUT | `/api/projects/<project_id>` | Update project |
| DELETE | `/api/projects/<project_id>` | Delete project |
| GET | `/api/projects/<project_id>/tasks` | Get project tasks |
| GET | `/api/projects/<project_id>/members` | Get project team members |
| GET | `/api/projects/<project_id>/stats` | Get project statistics |

### Tasks

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tasks` | Get all tasks |
| GET | `/api/tasks?enrich=true` | Get tasks with assignee/project names |
| GET | `/api/tasks?status=Pending` | Filter by status |
| GET | `/api/tasks?assignee_id=e03` | Filter by assignee |
| GET | `/api/tasks?project_id=p01` | Filter by project |
| GET | `/api/tasks/<task_id>` | Get specific task |
| POST | `/api/tasks` | Create new task |
| PUT | `/api/tasks/<task_id>` | Update task |
| PATCH | `/api/tasks/<task_id>/status` | Update task status only |
| DELETE | `/api/tasks/<task_id>` | Delete task |
| GET | `/api/tasks/by-assignee/<employee_id>` | Get tasks by assignee |
| GET | `/api/tasks/by-project/<project_id>` | Get tasks by project |
| GET | `/api/tasks/stats` | Get task statistics |

## API Usage Examples

### Create a new employee

```bash
curl -X POST http://localhost:5000/api/employees \
  -H "Content-Type: application/json" \
  -d '{
    "employee_id": "e07",
    "name": "John Doe",
    "role": "Frontend Developer",
    "user_role": "executor",
    "avatar": "JD",
    "capacity_hours_per_week": 40,
    "skills": [{"name": "react", "level": 5}]
  }'
```

### Create a new project

```bash
curl -X POST http://localhost:5000/api/projects \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "p06",
    "name": "New Project",
    "description": "Project description",
    "status": "Planning",
    "dueDate": "2025-12-31",
    "budget": 75000,
    "priority": "high"
  }'
```

### Create a new task

```bash
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "t16",
    "title": "New Task",
    "description": "Task description",
    "project_id": "p01",
    "assignee_id": "e03",
    "dueDate": "2025-11-30",
    "priority": "medium",
    "estimatedHours": 8
  }'
```

### Get enriched tasks (with names)

```bash
curl http://localhost:5000/api/tasks?enrich=true
```

### Update task status

```bash
curl -X PATCH http://localhost:5000/api/tasks/t01/status \
  -H "Content-Type: application/json" \
  -d '{"status": "Completed"}'
```

## Data Models

### Employee

```python
{
  "employee_id": "e01",
  "name": "Michael Chen",
  "role": "Backend Engineer",
  "user_role": "executor",  # pm or executor
  "avatar": "MC",
  "capacity_hours_per_week": 40,
  "current_load_hours": 35,
  "integrations": {
    "email": "michael.chen@codelllama.ai",
    "jira_account_id": "5f9c-e03",
    "slack_user_id": "U03GHI"
  },
  "languages": ["en", "zh"],
  "skills": [
    {"name": "python", "level": 5},
    {"name": "fastapi", "level": 5}
  ],
  "timezone": "Asia/Shanghai"
}
```

### Project

```python
{
  "project_id": "p01",
  "name": "Website Redesign",
  "description": "Complete redesign of company website",
  "status": "In Progress",  # Planning, In Progress, On Hold, Completed
  "budget": 50000,
  "priority": "high",  # low, medium, high, critical
  "dueDate": "2025-11-15",
  "createdAt": "2025-09-01",
  "tasksCount": 3,
  "completedTasks": 0
}
```

### Task

```python
{
  "task_id": "t01",
  "title": "Design homepage mockup",
  "description": "Create high-fidelity mockup",
  "status": "In Progress",  # Pending, In Progress, Completed, Blocked
  "priority": "high",  # low, medium, high, critical
  "assignee_id": "e04",
  "project_id": "p01",
  "estimatedHours": 8,
  "dueDate": "2025-10-28",
  "createdAt": "2025-10-15",
  "completedAt": null,
  
  # When enrich=true
  "assignee": "Emily Davis",
  "project": "Website Redesign"
}
```

## Frontend Integration

The backend is fully compatible with the provided React frontend. To connect:

1. Update frontend API base URL (if needed):
```javascript
const API_BASE_URL = 'http://localhost:5000/api'
```

2. The API supports CORS for origins specified in `.env`:
```env
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

3. All endpoints return enriched data compatible with frontend expectations:
   - Tasks include `assignee` and `project` names when `enrich=true`
   - Projects include `tasksCount` and `completedTasks`
   - Dates are in ISO format matching frontend expectations

## Database Schema

```
employees
├── employee_id (PK)
├── name
├── role
├── user_role
├── avatar
├── capacity_hours_per_week
├── current_load_hours
├── integrations (JSON)
├── languages (JSON)
├── skills (JSON)
└── timezone

projects
├── project_id (PK)
├── name (unique)
├── description
├── status
├── budget
├── priority
├── due_date
├── created_at
└── updated_at

tasks
├── task_id (PK)
├── title
├── description
├── status
├── priority
├── assignee_id (FK → employees)
├── project_id (FK → projects)
├── estimated_hours
├── due_date
├── created_at
├── completed_at
└── updated_at
```

## Development

### Running in development mode

```bash
export FLASK_ENV=development
python app.py
```

### Using Flask shell

```bash
flask shell

# Now you can interact with models:
>>> Employee.query.all()
>>> Project.query.filter_by(status='In Progress').all()
>>> db.session.add(new_task)
>>> db.session.commit()
```

### Creating migrations

```bash
# After model changes
flask db migrate -m "Description of changes"
flask db upgrade
```

## Production Deployment

### Using Gunicorn

```bash
pip install gunicorn

gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Environment Variables for Production

```env
FLASK_ENV=production
DATABASE_URL=postgresql://user:pass@host:5432/dbname
SECRET_KEY=your-production-secret-key
DEBUG=False
```

### Docker (Optional)

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

Run:
```bash
docker build -t planllama-backend .
docker run -p 5000:5000 planllama-backend
```

## Testing

Create a test file `test_api.py`:

```python
import unittest
from app import create_app
from extensions import db

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
    
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_get_employees(self):
        response = self.client.get('/api/employees')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
```

Run tests:
```bash
python test_api.py
```

## Troubleshooting

### Database connection errors

- Check PostgreSQL is running: `sudo service postgresql status`
- Verify DATABASE_URL in `.env`
- For SQLite, check file permissions

### CORS errors

- Verify frontend URL in CORS_ORIGINS
- Check browser console for specific error
- Ensure preflight requests are allowed

### Migration errors

```bash
# Reset migrations (development only)
rm -rf migrations/
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

## License

MIT License

## Support

For issues and questions, please create an issue on GitHub.
