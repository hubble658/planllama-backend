# PlanLLaMA Backend - Project Structure

```
backend/
│
├── 📄 app.py                          # Main Flask application
├── 📄 config.py                       # Configuration settings
├── 📄 extensions.py                   # Flask extensions (db, migrate, cors)
├── 📄 models.py                       # SQLAlchemy models (Employee, Project, Task)
├── 📄 seed.py                         # Database seed data
├── 📄 init_db.py                      # Database initialization script
│
├── 📁 routes/                         # API route blueprints
│   ├── employees.py                   # Employee endpoints
│   ├── projects.py                    # Project endpoints
│   └── tasks.py                       # Task endpoints
│
├── 📄 requirements.txt                # Python dependencies
├── 📄 .env.example                    # Environment variables template
├── 📄 .gitignore                      # Git ignore rules
│
├── 📄 README.md                       # Full documentation
├── 📄 QUICKSTART.md                   # Quick start guide
├── 📄 PROJECT_STRUCTURE.md            # This file
│
├── 🔧 run.sh                          # Auto-setup script (Linux/macOS)
├── 🔧 run.bat                         # Auto-setup script (Windows)
├── 🧪 test_api.py                     # API testing script
└── 📮 PlanLLaMA_API.postman_collection.json  # Postman collection

Generated at runtime:
├── 📁 migrations/                     # Database migrations (if using Flask-Migrate)
├── 📁 venv/                          # Virtual environment
├── 📄 .env                           # Your environment variables
└── 📄 planllama.db                   # SQLite database (if not using PostgreSQL)
```

## Key Files Explained

### Core Application Files

**app.py**
- Main Flask application factory
- Blueprint registration
- Error handlers
- Shell context

**models.py**
- Employee: Users (PMs and Executors)
- Project: Projects with tasks
- Task: Individual work items
- Relationships and data validation

**config.py**
- Environment-based configuration
- Database settings
- CORS configuration

**extensions.py**
- SQLAlchemy (database ORM)
- Flask-Migrate (database migrations)
- Flask-CORS (cross-origin support)

### Routes (API Endpoints)

**routes/employees.py**
```
GET    /api/employees                    # List all employees
GET    /api/employees?role=pm            # Filter by role
GET    /api/employees/<id>               # Get specific employee
POST   /api/employees                    # Create employee
PUT    /api/employees/<id>               # Update employee
DELETE /api/employees/<id>               # Delete employee
GET    /api/employees/<id>/workload      # Get workload stats
```

**routes/projects.py**
```
GET    /api/projects                     # List all projects
GET    /api/projects?status=In Progress  # Filter by status
GET    /api/projects/<id>                # Get specific project
POST   /api/projects                     # Create project
PUT    /api/projects/<id>                # Update project
DELETE /api/projects/<id>                # Delete project
GET    /api/projects/<id>/tasks          # Get project tasks
GET    /api/projects/<id>/members        # Get team members
GET    /api/projects/<id>/stats          # Get statistics
```

**routes/tasks.py**
```
GET    /api/tasks                        # List all tasks
GET    /api/tasks?enrich=true            # Tasks with names
GET    /api/tasks?status=Pending         # Filter by status
GET    /api/tasks?assignee_id=e03        # Filter by assignee
GET    /api/tasks/<id>                   # Get specific task
POST   /api/tasks                        # Create task
PUT    /api/tasks/<id>                   # Update task
PATCH  /api/tasks/<id>/status            # Update status only
DELETE /api/tasks/<id>                   # Delete task
GET    /api/tasks/by-assignee/<id>       # Tasks by assignee
GET    /api/tasks/by-project/<id>        # Tasks by project
GET    /api/tasks/stats                  # Get statistics
```

### Database & Setup

**seed.py**
- Initial data for development
- 6 employees, 5 projects, 15 tasks
- Matches frontend mock data

**init_db.py**
- Creates database tables
- Optionally seeds data
- Usage: `python init_db.py --seed`

### Utilities

**run.sh / run.bat**
- One-command setup and run
- Creates venv, installs deps, seeds DB
- Auto-configures environment

**test_api.py**
- Automated endpoint testing
- Tests all CRUD operations
- Usage: `python test_api.py`

**PlanLLaMA_API.postman_collection.json**
- Postman collection
- Pre-configured requests
- Import and test immediately

## Data Models Detail

### Employee Model
```python
{
  employee_id: str (PK)          # 'e01', 'e02', etc.
  name: str
  role: str                      # Job title
  user_role: str                 # 'pm' or 'executor'
  avatar: str                    # Initials
  capacity_hours_per_week: int
  current_load_hours: int
  integrations: JSON             # email, jira, slack
  languages: JSON                # ['en', 'tr']
  skills: JSON                   # [{'name': 'python', 'level': 5}]
  timezone: str
}
```

### Project Model
```python
{
  project_id: str (PK)           # 'p01', 'p02', etc.
  name: str (unique)
  description: str
  status: str                    # Planning, In Progress, etc.
  budget: int
  priority: str                  # low, medium, high, critical
  due_date: date
  created_at: datetime
  updated_at: datetime
  tasks: [Task]                  # Relationship
}
```

### Task Model
```python
{
  task_id: str (PK)              # 't01', 't02', etc.
  title: str
  description: str
  status: str                    # Pending, In Progress, etc.
  priority: str                  # low, medium, high, critical
  assignee_id: str (FK)          # → Employee
  project_id: str (FK)           # → Project
  estimated_hours: float
  due_date: date
  created_at: datetime
  completed_at: datetime
  updated_at: datetime
  assignee: Employee             # Relationship
  project: Project               # Relationship
}
```

## Database Relationships

```
Employee (1) ←─── (N) Task
Project  (1) ←─── (N) Task

Employee.assigned_tasks → [Task]
Task.assignee → Employee
Task.project → Project
Project.tasks → [Task]
```

## Environment Variables

**.env file:**
```env
DATABASE_URL=postgresql://user:pass@host/db
# or
DATABASE_URL=sqlite:///planllama.db

FLASK_ENV=development
SECRET_KEY=your-secret-key
DEBUG=True
PORT=5000
CORS_ORIGINS=http://localhost:5173
```

## Development Workflow

1. **Start Server**: `./run.sh` or `python app.py`
2. **Test APIs**: `python test_api.py`
3. **Shell Access**: `flask shell`
4. **Reset DB**: `rm planllama.db && python init_db.py --seed`
5. **Migrations**: `flask db migrate -m "message" && flask db upgrade`

## Frontend Integration Points

### Data Compatibility
- ✅ Task IDs match (`t01`, `t02`)
- ✅ Project IDs match (`p01`, `p02`)
- ✅ Employee IDs match (`e01`, `e02`)
- ✅ Date formats (ISO 8601)
- ✅ Enriched data with names

### Required Frontend Changes
```javascript
// Replace mock data imports with API calls
import { tasks } from '../data/tasks'  // ❌ Remove

// With API calls
const API_BASE = 'http://localhost:5000/api'
fetch(`${API_BASE}/tasks?enrich=true`)  // ✅ Add
```

### Example Integration
```javascript
// Get enriched tasks (with assignee and project names)
const response = await fetch('http://localhost:5000/api/tasks?enrich=true')
const tasks = await response.json()
// Returns same structure as frontend mock data

// Create new task
await fetch('http://localhost:5000/api/tasks', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    task_id: 't16',
    title: 'New Task',
    project_id: 'p01',
    assignee_id: 'e03',
    dueDate: '2025-11-30',
    priority: 'medium',
    estimatedHours: 8
  })
})
```

## Production Deployment

### Using PostgreSQL
```bash
# Install PostgreSQL
# Update .env
DATABASE_URL=postgresql://user:pass@localhost/planllama

# Run migrations
flask db upgrade
python -c "from app import app; from seed import seed_database; app.app_context().push(); seed_database()"
```

### Using Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Using Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## Testing Strategy

1. **Unit Tests**: Test individual model methods
2. **Integration Tests**: Test API endpoints
3. **Manual Testing**: Use Postman collection
4. **Automated Testing**: Use test_api.py script

## Security Considerations

- ✅ Input validation on all endpoints
- ✅ Foreign key constraints
- ✅ Error handling and rollback
- ⚠️ Add authentication for production
- ⚠️ Add rate limiting
- ⚠️ Add input sanitization
- ⚠️ Use environment secrets

## Performance Optimization

- Index frequently queried fields
- Use pagination for large datasets
- Cache static data
- Optimize queries with joins
- Use connection pooling

## Monitoring & Logging

```python
# Add logging
import logging
logging.basicConfig(level=logging.INFO)

# Add request timing
from time import time
@app.before_request
def start_timer():
    g.start = time()

@app.after_request
def log_request(response):
    if hasattr(g, 'start'):
        duration = time() - g.start
        logging.info(f"{request.method} {request.path} {response.status_code} {duration:.3f}s")
    return response
```

## Common Issues & Solutions

**Issue**: Database locked
**Solution**: Close all connections, restart server

**Issue**: CORS errors
**Solution**: Check CORS_ORIGINS in .env

**Issue**: Port in use
**Solution**: Change PORT in .env or kill process

**Issue**: Module not found
**Solution**: Activate venv and reinstall requirements

## Support & Resources

- 📖 README.md - Full documentation
- 🚀 QUICKSTART.md - Get started fast
- 🧪 test_api.py - Test all endpoints
- 📮 Postman collection - Interactive testing
- 🐛 GitHub Issues - Report problems
