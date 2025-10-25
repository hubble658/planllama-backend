# PlanLLaMA - System Architecture

## Complete System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        FRONTEND                              │
│                    (React + Vite)                            │
│                                                              │
│  ├─ Components                                              │
│  │  ├─ Dashboard                                            │
│  │  ├─ ProjectList / ProjectCard                           │
│  │  ├─ TaskList / TaskCard                                 │
│  │  └─ Modals (Task, Project)                              │
│  │                                                          │
│  ├─ Services                                                │
│  │  └─ api.js (API client)                                 │
│  │                                                          │
│  └─ Context                                                 │
│     └─ EmployeeContext                                      │
│                                                              │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   │ HTTP/JSON
                   │ (CORS enabled)
                   │
┌──────────────────▼──────────────────────────────────────────┐
│                        BACKEND API                           │
│                   (Flask + SQLAlchemy)                       │
│                                                              │
│  ├─ API Routes                                              │
│  │  ├─ /api/employees/*                                     │
│  │  ├─ /api/projects/*                                      │
│  │  └─ /api/tasks/*                                         │
│  │                                                          │
│  ├─ Business Logic                                          │
│  │  ├─ Data validation                                      │
│  │  ├─ Relationships                                        │
│  │  └─ Enrichment (IDs → Names)                            │
│  │                                                          │
│  └─ Extensions                                              │
│     ├─ CORS                                                 │
│     ├─ SQLAlchemy ORM                                       │
│     └─ Flask-Migrate                                        │
│                                                              │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   │ SQL Queries
                   │
┌──────────────────▼──────────────────────────────────────────┐
│                       DATABASE                               │
│              (PostgreSQL / SQLite)                           │
│                                                              │
│  ┌────────────────────────────────────────────────┐         │
│  │ employees                                      │         │
│  │ ├─ employee_id (PK)                            │         │
│  │ ├─ name, role, user_role                       │         │
│  │ ├─ capacity, workload                          │         │
│  │ └─ skills, integrations (JSON)                 │         │
│  └────────────────────────────────────────────────┘         │
│                         │                                    │
│                         │ 1:N                                │
│                         │                                    │
│  ┌────────────────────────────────────────────────┐         │
│  │ tasks                                          │         │
│  │ ├─ task_id (PK)                                │         │
│  │ ├─ title, description                          │         │
│  │ ├─ status, priority                            │         │
│  │ ├─ assignee_id (FK → employees)                │         │
│  │ ├─ project_id (FK → projects)                  │         │
│  │ └─ dates, hours                                │         │
│  └────────────────────────────────────────────────┘         │
│                         │                                    │
│                         │ N:1                                │
│                         │                                    │
│  ┌────────────────────────────────────────────────┐         │
│  │ projects                                       │         │
│  │ ├─ project_id (PK)                             │         │
│  │ ├─ name, description                           │         │
│  │ ├─ status, priority                            │         │
│  │ └─ budget, dates                               │         │
│  └────────────────────────────────────────────────┘         │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Data Flow Examples

### 1. Get Tasks for Project Manager Dashboard

```
Frontend                    Backend                     Database
   │                          │                            │
   │ GET /api/tasks?          │                            │
   │ enrich=true              │                            │
   ├────────────────────────► │                            │
   │                          │ SELECT * FROM tasks        │
   │                          ├──────────────────────────► │
   │                          │                            │
   │                          │ ◄────────────────────────┤ │
   │                          │ [tasks with IDs]           │
   │                          │                            │
   │                          │ JOIN employees,projects    │
   │                          │ to get names               │
   │                          ├──────────────────────────► │
   │                          │                            │
   │                          │ ◄────────────────────────┤ │
   │ ◄────────────────────────┤                            │
   │ [tasks with names]       │                            │
   │                          │                            │
```

### 2. Create New Task

```
Frontend                    Backend                     Database
   │                          │                            │
   │ POST /api/tasks          │                            │
   │ {task data}              │                            │
   ├────────────────────────► │                            │
   │                          │ Validate data              │
   │                          │ Check FK exists            │
   │                          │                            │
   │                          │ INSERT INTO tasks          │
   │                          ├──────────────────────────► │
   │                          │                            │
   │                          │ ◄────────────────────────┤ │
   │                          │ Update project             │
   │                          │ task counts                │
   │                          │                            │
   │                          │ SELECT enriched data       │
   │                          ├──────────────────────────► │
   │                          │                            │
   │                          │ ◄────────────────────────┤ │
   │ ◄────────────────────────┤                            │
   │ {created task}           │                            │
   │                          │                            │
```

### 3. Update Task Status (Executor)

```
Frontend                    Backend                     Database
   │                          │                            │
   │ PATCH /api/tasks/t01/    │                            │
   │ status {"status":"Done"} │                            │
   ├────────────────────────► │                            │
   │                          │ UPDATE tasks               │
   │                          │ SET status='Completed',    │
   │                          │ completed_at=NOW()         │
   │                          ├──────────────────────────► │
   │                          │                            │
   │                          │ ◄────────────────────────┤ │
   │                          │ SELECT updated task        │
   │                          ├──────────────────────────► │
   │                          │                            │
   │                          │ ◄────────────────────────┤ │
   │ ◄────────────────────────┤                            │
   │ {updated task}           │                            │
   │                          │                            │
```

## API Request/Response Flow

### Enriched Task Request

**Frontend Request:**
```javascript
fetch('http://localhost:5000/api/tasks?enrich=true&status=In Progress')
```

**Backend Processing:**
```python
1. Parse query parameters
   - enrich = true
   - status = "In Progress"

2. Query database
   tasks = Task.query.filter_by(status='In Progress').all()

3. Enrich data (add names)
   for task in tasks:
       task.assignee = Employee.query.get(task.assignee_id).name
       task.project = Project.query.get(task.project_id).name

4. Return JSON
   return jsonify([task.to_dict(enrich=True) for task in tasks])
```

**Response to Frontend:**
```json
[
  {
    "task_id": "t01",
    "title": "Design homepage mockup",
    "assignee_id": "e04",
    "project_id": "p01",
    "assignee": "Emily Davis",     // ← Enriched
    "project": "Website Redesign", // ← Enriched
    "status": "In Progress",
    ...
  }
]
```

## Component Integration Pattern

### Example: TaskList Component

```javascript
// 1. Component mounts
useEffect(() => {
  loadTasks()
}, [])

// 2. Fetch from API
const loadTasks = async () => {
  const tasks = await api.getTasks({ status: 'In Progress' })
  setTasks(tasks)
}

// 3. User creates task
const handleCreate = async (taskData) => {
  const created = await api.createTask(taskData)
  setTasks([...tasks, created])
}

// 4. User updates task
const handleUpdate = async (taskId, data) => {
  const updated = await api.updateTask(taskId, data)
  setTasks(tasks.map(t => t.task_id === taskId ? updated : t))
}

// 5. User deletes task
const handleDelete = async (taskId) => {
  await api.deleteTask(taskId)
  setTasks(tasks.filter(t => t.task_id !== taskId))
}
```

## Database Relationships

```
Employee (1) ──────── (N) Task
   │
   └─ assigned_tasks: [Task]

Task (N) ──────── (1) Employee
   │                     └─ assignee
   │
   └─ (N) ──────── (1) Project
                        └─ project

Project (1) ──────── (N) Task
   │
   └─ tasks: [Task]
```

## Security & Validation

### Input Validation Flow

```
Frontend Input
     │
     ▼
Client-side Validation (React)
     │
     ▼
API Request
     │
     ▼
Backend Validation (Flask)
  ├─ Required fields check
  ├─ Data type validation
  ├─ Foreign key existence
  └─ Business logic validation
     │
     ▼
Database Constraints
  ├─ Primary key uniqueness
  ├─ Foreign key integrity
  └─ NOT NULL constraints
     │
     ▼
Data Saved
```

### Error Handling

```
Database Error
     │
     ▼
SQLAlchemy catches error
     │
     ▼
Flask error handler
  ├─ Rollback transaction
  ├─ Log error
  └─ Return JSON error
     │
     ▼
Frontend receives error
     │
     ▼
Display user message
```

## Deployment Architecture

### Development
```
Frontend (Vite)          Backend (Flask Dev)      Database (SQLite)
localhost:5173    ────►  localhost:5000    ────►  planllama.db
```

### Production
```
Frontend (Nginx)         Backend (Gunicorn)       Database (PostgreSQL)
yourdomain.com    ────►  api.yourdomain.com ────► postgres.server
     │                         │                         │
     │                         │                         │
  HTTPS                    HTTPS                   SSL/TLS
     │                         │                         │
Load Balancer            Load Balancer            Replication
     │                         │                         │
  [Server 1]              [Worker 1-4]            [Primary]
  [Server 2]                                      [Replica 1]
                                                  [Replica 2]
```

## Performance Optimization

### Query Optimization
```python
# ❌ Bad: N+1 queries
tasks = Task.query.all()
for task in tasks:
    print(task.assignee.name)  # Separate query each time

# ✅ Good: Eager loading
tasks = Task.query.options(
    joinedload(Task.assignee),
    joinedload(Task.project)
).all()
for task in tasks:
    print(task.assignee.name)  # Already loaded
```

### Caching Strategy
```python
from flask_caching import Cache

cache = Cache(config={'CACHE_TYPE': 'simple'})

@app.route('/api/employees')
@cache.cached(timeout=300)  # Cache for 5 minutes
def get_employees():
    return jsonify([emp.to_dict() for emp in Employee.query.all()])
```

## Monitoring & Logging

### Request Logging
```python
@app.before_request
def log_request():
    app.logger.info(f'{request.method} {request.path}')

@app.after_request
def log_response(response):
    app.logger.info(f'Response: {response.status_code}')
    return response
```

### Error Tracking
```python
@app.errorhandler(Exception)
def handle_error(error):
    app.logger.error(f'Error: {error}', exc_info=True)
    return jsonify({'error': 'Internal server error'}), 500
```

## Scalability Considerations

### Horizontal Scaling
```
Load Balancer
     │
     ├─► Backend Instance 1
     ├─► Backend Instance 2
     ├─► Backend Instance 3
     └─► Backend Instance 4
           │
           ▼
     Shared Database
```

### Database Scaling
```
Application Servers
     │
     ▼
Connection Pool
     │
     ├─► Read Replica 1 (Read queries)
     ├─► Read Replica 2 (Read queries)
     └─► Primary DB (Write queries)
```

## API Versioning Strategy

```
/api/v1/tasks    # Current version
/api/v2/tasks    # New version (backward compatible)

# Blueprint structure:
routes/
  ├─ v1/
  │  ├─ tasks.py
  │  └─ projects.py
  └─ v2/
     ├─ tasks.py
     └─ projects.py
```

## Testing Architecture

```
Unit Tests (models.py)
  ├─ Test Employee model
  ├─ Test Project model
  └─ Test Task model
     │
     ▼
Integration Tests (routes/)
  ├─ Test employee endpoints
  ├─ Test project endpoints
  └─ Test task endpoints
     │
     ▼
End-to-End Tests
  └─ Test complete workflows
```

## Summary

This architecture provides:
- ✅ **Separation of Concerns**: Frontend, Backend, Database
- ✅ **RESTful Design**: Standard HTTP methods and status codes
- ✅ **Data Integrity**: Foreign keys and constraints
- ✅ **Scalability**: Horizontal and vertical scaling options
- ✅ **Maintainability**: Clear structure and documentation
- ✅ **Security**: Input validation and error handling
- ✅ **Performance**: Query optimization and caching
- ✅ **Flexibility**: Easy to extend and modify
