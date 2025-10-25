# 🚀 Quick Start Guide

Get PlanLLaMA backend running in 5 minutes!

## Option 1: Automatic Setup (Recommended)

### macOS/Linux:
```bash
chmod +x run.sh
./run.sh
```

### Windows:
```bash
run.bat
```

That's it! The script will:
- ✅ Create virtual environment
- ✅ Install dependencies
- ✅ Create .env file
- ✅ Initialize database with sample data
- ✅ Start the server

## Option 2: Manual Setup

### 1. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup environment
```bash
cp .env.example .env
# Edit .env if needed (default SQLite works fine for development)
```

### 4. Initialize database
```bash
python init_db.py --seed
```

### 5. Run the server
```bash
python app.py
```

## Verify Installation

### Test in Browser
Open: http://localhost:5000

You should see:
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

### Run Automated Tests
```bash
python test_api.py
```

### Import Postman Collection
1. Open Postman
2. Import `PlanLLaMA_API.postman_collection.json`
3. Start testing!

## Common Commands

```bash
# View all employees
curl http://localhost:5000/api/employees

# View all projects
curl http://localhost:5000/api/projects

# View all tasks (with names)
curl http://localhost:5000/api/tasks?enrich=true

# View tasks for specific employee
curl http://localhost:5000/api/tasks/by-assignee/e03

# Get project statistics
curl http://localhost:5000/api/projects/p01/stats
```

## Frontend Integration

Update your frontend API configuration:

```javascript
// In your React app
const API_BASE_URL = 'http://localhost:5000/api'

// Example API calls
fetch(`${API_BASE_URL}/employees`)
fetch(`${API_BASE_URL}/projects`)
fetch(`${API_BASE_URL}/tasks?enrich=true`)
```

## Database Management

### Reset database with fresh data
```bash
rm planllama.db  # Delete existing database
python init_db.py --seed
```

### Use Flask shell for queries
```bash
flask shell

# Interactive Python shell with database access
>>> from models import Employee, Project, Task
>>> Employee.query.all()
>>> Project.query.filter_by(status='In Progress').all()
```

## Troubleshooting

### Port already in use
```bash
# Change port in .env
PORT=5001

# Or kill existing process
lsof -ti:5000 | xargs kill -9  # macOS/Linux
```

### Database locked (SQLite)
```bash
# Close any other connections to the database
# Or simply restart
rm planllama.db
python init_db.py --seed
```

### Module not found
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

## Next Steps

1. ✅ Backend is running on http://localhost:5000
2. 🎨 Connect your frontend (update API_BASE_URL)
3. 📱 Test endpoints with Postman or test_api.py
4. 📖 Read full API docs in README.md
5. 🚀 Start building!

## Sample Data Included

The seed data includes:
- 6 employees (2 PMs, 4 executors)
- 5 projects (Website, Mobile App, API, E-commerce, DevOps)
- 15 tasks across all projects

Perfect for testing your frontend!

## Support

- 📖 Full docs: `README.md`
- 🧪 Test script: `python test_api.py`
- 📮 Postman collection: Import the JSON file
- 🐛 Issues: Create GitHub issue
