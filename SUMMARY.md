# 🎉 PlanLLaMA Backend - Complete Package

## What You Got

A **production-ready Flask backend** that is **100% compatible** with your React frontend!

### ✨ Features

✅ **Complete REST API** with all CRUD operations  
✅ **PostgreSQL + SQLAlchemy** for robust data management  
✅ **Fully compatible** with your existing frontend  
✅ **Database migrations** with Flask-Migrate  
✅ **CORS enabled** for seamless frontend integration  
✅ **Seeded database** with 6 employees, 5 projects, 15 tasks  
✅ **Enriched responses** that match frontend expectations  
✅ **Comprehensive documentation** and examples  
✅ **Testing suite** included  
✅ **One-command setup** scripts  

## 📁 Package Contents

```
backend/
├── 📖 Documentation
│   ├── README.md                    # Complete API documentation
│   ├── QUICKSTART.md               # Get started in 5 minutes
│   ├── PROJECT_STRUCTURE.md        # Architecture overview
│   └── FRONTEND_INTEGRATION.md     # How to connect frontend
│
├── 🔧 Core Application
│   ├── app.py                      # Main Flask application
│   ├── config.py                   # Configuration management
│   ├── extensions.py               # Flask extensions (DB, CORS)
│   ├── models.py                   # Database models
│   └── seed.py                     # Sample data
│
├── 🛣️ API Routes
│   ├── routes/employees.py         # Employee endpoints
│   ├── routes/projects.py          # Project endpoints
│   └── routes/tasks.py             # Task endpoints
│
├── 🚀 Setup & Testing
│   ├── run.sh                      # Auto-setup (Linux/macOS)
│   ├── run.bat                     # Auto-setup (Windows)
│   ├── init_db.py                  # Database initialization
│   ├── test_api.py                 # Automated tests
│   └── PlanLLaMA_API.postman_collection.json
│
├── ⚙️ Configuration
│   ├── requirements.txt            # Python dependencies
│   ├── .env.example               # Environment template
│   └── .gitignore                 # Git ignore rules
```

## 🚀 Quick Start (Choose One)

### Option A: Automatic Setup (Recommended)

**macOS/Linux:**
```bash
cd backend
chmod +x run.sh
./run.sh
```

**Windows:**
```bash
cd backend
run.bat
```

✨ **That's it!** The script handles everything:
- Creates virtual environment
- Installs dependencies
- Sets up database
- Seeds sample data
- Starts server at http://localhost:5000

### Option B: Manual Setup

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup environment
cp .env.example .env

# 4. Initialize database with sample data
python init_db.py --seed

# 5. Start server
python app.py
```

## 🧪 Verify Installation

### Test in Browser
Visit: http://localhost:5000

Expected response:
```json
{
  "message": "PlanLLaMA API",
  "version": "1.0.0",
  "endpoints": {
    "employees": "/api/employees",
    "projects": "/api/projects",
    "tasks": "/api/tasks"
  }
}
```

### Run Test Suite
```bash
python test_api.py
```

### Import Postman Collection
1. Open Postman
2. Import `PlanLLaMA_API.postman_collection.json`
3. Test all endpoints interactively

## 📊 API Overview

### Employees API
```
GET    /api/employees              # All employees
GET    /api/employees?role=pm      # Filter by role
GET    /api/employees/<id>         # Specific employee
POST   /api/employees              # Create
PUT    /api/employees/<id>         # Update
DELETE /api/employees/<id>         # Delete
GET    /api/employees/<id>/workload # Stats
```

### Projects API
```
GET    /api/projects               # All projects
GET    /api/projects?status=...    # Filter by status
GET    /api/projects/<id>          # Specific project
POST   /api/projects               # Create
PUT    /api/projects/<id>          # Update
DELETE /api/projects/<id>          # Delete
GET    /api/projects/<id>/tasks    # Project tasks
GET    /api/projects/<id>/members  # Team members
GET    /api/projects/<id>/stats    # Statistics
```

### Tasks API
```
GET    /api/tasks                  # All tasks
GET    /api/tasks?enrich=true      # With names (recommended)
GET    /api/tasks?status=...       # Filter by status
GET    /api/tasks?assignee_id=...  # Filter by assignee
GET    /api/tasks/<id>             # Specific task
POST   /api/tasks                  # Create
PUT    /api/tasks/<id>             # Update
PATCH  /api/tasks/<id>/status      # Update status only
DELETE /api/tasks/<id>             # Delete
GET    /api/tasks/by-assignee/<id> # By assignee
GET    /api/tasks/by-project/<id>  # By project
GET    /api/tasks/stats            # Statistics
```

## 🔗 Frontend Integration

### Step 1: Create API Service (Frontend)

Save as `src/services/api.js`:

```javascript
const API_BASE = 'http://localhost:5000/api'

export default {
  // Get all tasks with assignee and project names
  getTasks: () => 
    fetch(`${API_BASE}/tasks?enrich=true`).then(r => r.json()),
  
  // Get all projects
  getProjects: () => 
    fetch(`${API_BASE}/projects`).then(r => r.json()),
  
  // Get all employees
  getEmployees: () => 
    fetch(`${API_BASE}/employees`).then(r => r.json()),
  
  // Create task
  createTask: (data) =>
    fetch(`${API_BASE}/tasks`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    }).then(r => r.json()),
  
  // Update task
  updateTask: (id, data) =>
    fetch(`${API_BASE}/tasks/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    }).then(r => r.json())
}
```

### Step 2: Use in Components

**Before** (mock data):
```javascript
import { tasks } from '../data/tasks'
const [tasks, setTasks] = useState(getEnrichedTasks())
```

**After** (API):
```javascript
import api from '../services/api'

useEffect(() => {
  api.getTasks().then(setTasks)
}, [])
```

See `FRONTEND_INTEGRATION.md` for complete examples!

## 💾 Sample Data Included

The database is pre-seeded with:

**6 Employees:**
- 2 Project Managers (Sarah Johnson, David Wilson)
- 4 Executors (Michael Chen, Emily Davis, Alex Kumar, Yavuz Kaya)

**5 Projects:**
- Website Redesign (3 tasks)
- Mobile App Development (4 tasks)
- API Integration (3 tasks)
- E-commerce Platform (3 tasks)
- DevOps (2 tasks)

**15 Tasks:**
- Various statuses (Pending, In Progress, Completed)
- Different priorities (low, medium, high, critical)
- Assigned to different employees

All data matches your frontend mock data structure!

## 🎯 Key Features

### 1. Enriched Data Responses
Tasks automatically include assignee and project names when using `?enrich=true`:

```javascript
{
  "task_id": "t01",
  "title": "Design homepage mockup",
  "assignee_id": "e04",      // For backend use
  "project_id": "p01",       // For backend use
  "assignee": "Emily Davis", // ✅ Frontend uses this
  "project": "Website Redesign" // ✅ Frontend uses this
}
```

### 2. Automatic Calculations
Projects automatically calculate task counts:

```javascript
{
  "project_id": "p01",
  "name": "Website Redesign",
  "tasksCount": 3,        // ✅ Calculated automatically
  "completedTasks": 0     // ✅ Calculated automatically
}
```

### 3. Flexible Querying
Filter and search with query parameters:

```bash
# Get only pending tasks
/api/tasks?status=Pending&enrich=true

# Get tasks for specific employee
/api/tasks?assignee_id=e03&enrich=true

# Get tasks for specific project
/api/tasks?project_id=p01&enrich=true
```

### 4. CORS Pre-configured
Works seamlessly with React development server:

```env
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| **README.md** | Complete API reference, all endpoints, examples |
| **QUICKSTART.md** | Get started in 5 minutes |
| **PROJECT_STRUCTURE.md** | Architecture, data models, relationships |
| **FRONTEND_INTEGRATION.md** | Step-by-step integration guide |

## 🧪 Testing

### Automated Testing
```bash
python test_api.py
```

Tests all endpoints with:
- Creating records
- Reading/querying
- Updating
- Deleting
- Filtering
- Statistics

### Manual Testing with Postman
1. Import `PlanLLaMA_API.postman_collection.json`
2. Collection includes all endpoints
3. Pre-configured requests ready to run

### Interactive Testing
```bash
flask shell

>>> from models import Employee, Project, Task
>>> Employee.query.all()
>>> Task.query.filter_by(status='In Progress').all()
```

## 🔧 Database Options

### SQLite (Development - Default)
```env
DATABASE_URL=sqlite:///planllama.db
```
✅ No installation needed  
✅ Perfect for development  
✅ File-based, portable  

### PostgreSQL (Production)
```env
DATABASE_URL=postgresql://user:pass@localhost/planllama
```
✅ Production-ready  
✅ Better performance  
✅ Advanced features  

Setup PostgreSQL:
```bash
# Install PostgreSQL
# Create database
createdb planllama

# Update .env
DATABASE_URL=postgresql://username:password@localhost/planllama

# Run migrations
flask db upgrade

# Seed data
python -c "from app import app; from seed import seed_database; app.app_context().push(); seed_database()"
```

## 🚀 Production Deployment

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

### Environment for Production
```env
FLASK_ENV=production
DATABASE_URL=postgresql://user:pass@host/db
SECRET_KEY=your-production-secret-key
DEBUG=False
CORS_ORIGINS=https://yourdomain.com
```

## 🎓 Common Tasks

### Reset Database
```bash
rm planllama.db
python init_db.py --seed
```

### Add New Employee
```bash
curl -X POST http://localhost:5000/api/employees \
  -H "Content-Type: application/json" \
  -d '{
    "employee_id": "e07",
    "name": "Jane Doe",
    "role": "Developer",
    "user_role": "executor",
    "avatar": "JD"
  }'
```

### Create Project
```bash
curl -X POST http://localhost:5000/api/projects \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "p06",
    "name": "New Project",
    "dueDate": "2025-12-31",
    "status": "Planning"
  }'
```

### Get Employee Workload
```bash
curl http://localhost:5000/api/employees/e03/workload
```

## ❓ Troubleshooting

### Server won't start
```bash
# Check if port is in use
lsof -ti:5000 | xargs kill -9  # macOS/Linux

# Change port in .env
PORT=5001
```

### CORS errors
```bash
# Check CORS_ORIGINS in .env matches frontend URL
CORS_ORIGINS=http://localhost:5173
```

### Database errors
```bash
# Reset database
rm planllama.db
python init_db.py --seed
```

### Import errors
```bash
# Ensure virtual environment is activated
source venv/bin/activate
pip install -r requirements.txt
```

## 📞 Support

- 📖 Check documentation files
- 🧪 Run test suite: `python test_api.py`
- 📮 Test with Postman collection
- 🐛 Create GitHub issue

## 🎯 Next Steps

1. ✅ Start backend: `./run.sh`
2. ✅ Test API: `python test_api.py`
3. ✅ Import Postman collection
4. ✅ Read `FRONTEND_INTEGRATION.md`
5. ✅ Update frontend to use API
6. ✅ Build awesome features!

## 📦 What's Included

- ✅ Complete REST API backend
- ✅ Database models with relationships
- ✅ Sample data matching frontend
- ✅ Comprehensive documentation
- ✅ Testing suite
- ✅ Auto-setup scripts
- ✅ Postman collection
- ✅ Frontend integration guide
- ✅ Production deployment guide
- ✅ Error handling
- ✅ CORS configuration
- ✅ Migration support

## 💡 Tips

1. **Always use `enrich=true`** for tasks to get assignee/project names
2. **Check documentation** - everything is documented with examples
3. **Use Postman** for interactive testing
4. **Run test_api.py** to verify all endpoints work
5. **Read FRONTEND_INTEGRATION.md** for integration examples
6. **Start with SQLite** for development, switch to PostgreSQL for production

---

## 🎉 You're All Set!

Your backend is ready to power your PlanLLaMA frontend!

**Need help?** Check the documentation files - they have everything you need!

Happy coding! 🚀
