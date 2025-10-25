# Frontend Integration Guide

This guide shows you how to integrate your React frontend with the PlanLLaMA backend API.

## Quick Integration (3 Steps)

### Step 1: Start the Backend

```bash
cd backend
./run.sh    # or run.bat on Windows
```

Backend will run on: `http://localhost:5000`

### Step 2: Create API Service (Frontend)

Create `src/services/api.js`:

```javascript
const API_BASE_URL = 'http://localhost:5000/api'

class APIService {
  // Employees
  async getEmployees(role = null) {
    const url = role ? `${API_BASE_URL}/employees?role=${role}` : `${API_BASE_URL}/employees`
    const response = await fetch(url)
    return response.json()
  }

  async getEmployee(employeeId) {
    const response = await fetch(`${API_BASE_URL}/employees/${employeeId}`)
    return response.json()
  }

  // Projects
  async getProjects(options = {}) {
    const params = new URLSearchParams()
    if (options.status) params.append('status', options.status)
    if (options.include_tasks) params.append('include_tasks', 'true')
    
    const url = `${API_BASE_URL}/projects?${params}`
    const response = await fetch(url)
    return response.json()
  }

  async getProject(projectId, includeTasks = false) {
    const url = `${API_BASE_URL}/projects/${projectId}?include_tasks=${includeTasks}`
    const response = await fetch(url)
    return response.json()
  }

  async createProject(projectData) {
    const response = await fetch(`${API_BASE_URL}/projects`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(projectData)
    })
    return response.json()
  }

  async updateProject(projectId, projectData) {
    const response = await fetch(`${API_BASE_URL}/projects/${projectId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(projectData)
    })
    return response.json()
  }

  async deleteProject(projectId) {
    await fetch(`${API_BASE_URL}/projects/${projectId}`, {
      method: 'DELETE'
    })
  }

  // Tasks
  async getTasks(options = {}) {
    const params = new URLSearchParams({ enrich: 'true' })
    if (options.status) params.append('status', options.status)
    if (options.assignee_id) params.append('assignee_id', options.assignee_id)
    if (options.project_id) params.append('project_id', options.project_id)
    
    const url = `${API_BASE_URL}/tasks?${params}`
    const response = await fetch(url)
    return response.json()
  }

  async getTask(taskId) {
    const response = await fetch(`${API_BASE_URL}/tasks/${taskId}?enrich=true`)
    return response.json()
  }

  async createTask(taskData) {
    const response = await fetch(`${API_BASE_URL}/tasks`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(taskData)
    })
    return response.json()
  }

  async updateTask(taskId, taskData) {
    const response = await fetch(`${API_BASE_URL}/tasks/${taskId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(taskData)
    })
    return response.json()
  }

  async updateTaskStatus(taskId, status) {
    const response = await fetch(`${API_BASE_URL}/tasks/${taskId}/status`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status })
    })
    return response.json()
  }

  async deleteTask(taskId) {
    await fetch(`${API_BASE_URL}/tasks/${taskId}`, {
      method: 'DELETE'
    })
  }

  async getTasksByAssignee(assigneeId) {
    const response = await fetch(`${API_BASE_URL}/tasks/by-assignee/${assigneeId}`)
    return response.json()
  }

  async getTasksByProject(projectId) {
    const response = await fetch(`${API_BASE_URL}/tasks/by-project/${projectId}`)
    return response.json()
  }
}

export default new APIService()
```

### Step 3: Update Components to Use API

#### Example: TaskList Component

**Before** (using mock data):
```javascript
import { getEnrichedTasks } from '../data/tasks'

function TaskList({ role, project = null }) {
  const [tasks, setTasks] = useState(getEnrichedTasks())
  
  // ... rest of component
}
```

**After** (using API):
```javascript
import api from '../services/api'

function TaskList({ role, project = null }) {
  const [tasks, setTasks] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadTasks()
  }, [role, project])

  const loadTasks = async () => {
    try {
      setLoading(true)
      let data
      
      if (project) {
        // Get tasks for specific project
        const response = await api.getTasksByProject(
          // Convert project name to project_id if needed
          projects.find(p => p.name === project)?.project_id
        )
        data = response.tasks
      } else if (role === 'executor' && currentEmployee) {
        // Get tasks for current employee
        const response = await api.getTasksByAssignee(currentEmployee.employee_id)
        data = response.tasks
      } else {
        // Get all tasks
        data = await api.getTasks()
      }
      
      setTasks(data)
    } catch (error) {
      console.error('Error loading tasks:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSaveTask = async (taskData) => {
    try {
      if (editingTask) {
        await api.updateTask(taskData.task_id, taskData)
      } else {
        await api.createTask(taskData)
      }
      await loadTasks() // Reload tasks
    } catch (error) {
      console.error('Error saving task:', error)
    }
  }

  const handleDeleteTask = async (taskId) => {
    if (window.confirm('Are you sure?')) {
      try {
        await api.deleteTask(taskId)
        await loadTasks() // Reload tasks
      } catch (error) {
        console.error('Error deleting task:', error)
      }
    }
  }

  if (loading) return <div>Loading...</div>

  // ... rest of component
}
```

## Component-by-Component Migration

### ProjectList Component

```javascript
import { useEffect, useState } from 'react'
import api from '../services/api'

function ProjectList({ role }) {
  const [projects, setProjects] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadProjects()
  }, [])

  const loadProjects = async () => {
    try {
      setLoading(true)
      const data = await api.getProjects()
      setProjects(data)
    } catch (error) {
      console.error('Error loading projects:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSaveProject = async (project) => {
    try {
      if (editingProject) {
        await api.updateProject(project.project_id, project)
      } else {
        await api.createProject(project)
      }
      await loadProjects()
    } catch (error) {
      console.error('Error saving project:', error)
    }
  }

  const handleDeleteProject = async (projectId) => {
    if (window.confirm('Are you sure?')) {
      try {
        await api.deleteProject(projectId)
        await loadProjects()
      } catch (error) {
        console.error('Error deleting project:', error)
      }
    }
  }

  // ... rest of component
}
```

### Dashboard Component

```javascript
import { useEffect, useState, useMemo } from 'react'
import api from '../services/api'

function Dashboard({ role = 'pm' }) {
  const [projects, setProjects] = useState([])
  const [tasks, setTasks] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadData()
  }, [role, currentEmployee])

  const loadData = async () => {
    try {
      setLoading(true)
      const [projectsData, tasksData] = await Promise.all([
        api.getProjects(),
        role === 'executor' && currentEmployee
          ? api.getTasksByAssignee(currentEmployee.employee_id).then(r => r.tasks)
          : api.getTasks()
      ])
      
      setProjects(projectsData)
      setTasks(tasksData)
    } catch (error) {
      console.error('Error loading data:', error)
    } finally {
      setLoading(false)
    }
  }

  // Calculate stats from loaded data
  const stats = useMemo(() => {
    // ... calculate stats from projects and tasks
  }, [projects, tasks])

  // ... rest of component
}
```

### TaskModal Component - Handle Save

```javascript
const handleSubmit = async (e) => {
  e.preventDefault()

  // Get employee and project objects for the IDs
  const selectedEmployee = employees.find(emp => emp.name === formData.assignee)
  const selectedProject = projects.find(proj => proj.name === formData.project)

  const taskData = {
    task_id: task?.task_id || `t${Date.now()}`,
    title: formData.title,
    description: formData.description,
    status: formData.status,
    priority: formData.priority,
    assignee_id: selectedEmployee?.employee_id,
    project_id: selectedProject?.project_id,
    estimatedHours: parseFloat(formData.estimatedHours) || 0,
    dueDate: formData.dueDate
  }

  onSave(taskData) // Parent component will handle API call
  onClose()
}
```

## Error Handling

Create a custom hook for better error handling:

```javascript
// src/hooks/useAPI.js
import { useState } from 'react'

export function useAPI() {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const execute = async (apiCall) => {
    try {
      setLoading(true)
      setError(null)
      return await apiCall()
    } catch (err) {
      setError(err.message)
      console.error('API Error:', err)
      throw err
    } finally {
      setLoading(false)
    }
  }

  return { loading, error, execute }
}

// Usage:
function MyComponent() {
  const { loading, error, execute } = useAPI()

  const loadData = () => execute(() => api.getTasks())

  if (loading) return <div>Loading...</div>
  if (error) return <div>Error: {error}</div>
  // ...
}
```

## Data Format Compatibility

### Backend Response → Frontend Expected Format

The backend API is designed to return data in the exact format your frontend expects:

**Tasks (with enrich=true):**
```javascript
{
  task_id: "t01",
  title: "Design homepage mockup",
  description: "Create high-fidelity mockup",
  status: "In Progress",
  priority: "high",
  assignee_id: "e04",
  project_id: "p01",
  estimatedHours: 8,
  dueDate: "2025-10-28",
  
  // Enriched fields (when enrich=true)
  assignee: "Emily Davis",      // ✅ Frontend uses this
  project: "Website Redesign"   // ✅ Frontend uses this
}
```

**Projects:**
```javascript
{
  project_id: "p01",
  name: "Website Redesign",
  description: "Complete redesign",
  status: "In Progress",
  dueDate: "2025-11-15",
  createdAt: "2025-09-01",
  tasksCount: 3,              // ✅ Calculated automatically
  completedTasks: 0,          // ✅ Calculated automatically
  budget: 50000,
  priority: "high"
}
```

## ID Generation

When creating new entities, generate IDs:

```javascript
// For tasks
const newTaskId = `t${String(Date.now()).slice(-8)}`

// For projects  
const newProjectId = `p${String(Date.now()).slice(-8)}`

// Or let backend handle it by omitting the ID
```

## Common Integration Patterns

### Pattern 1: Load → Edit → Save
```javascript
// Load
const task = await api.getTask('t01')

// Edit locally
setFormData(task)

// Save
await api.updateTask('t01', updatedTask)
```

### Pattern 2: Optimistic Updates
```javascript
// Update UI immediately
setTasks(prev => prev.map(t => 
  t.task_id === taskId ? { ...t, status: 'Completed' } : t
))

// Then save to backend
try {
  await api.updateTaskStatus(taskId, 'Completed')
} catch (error) {
  // Rollback on error
  setTasks(originalTasks)
}
```

### Pattern 3: Cascade Refresh
```javascript
// After creating a task, refresh both tasks and project
await api.createTask(newTask)
await Promise.all([
  loadTasks(),
  loadProject(newTask.project_id)
])
```

## Testing Integration

### 1. Test Backend First
```bash
cd backend
python test_api.py
```

### 2. Test with Postman
Import `PlanLLaMA_API.postman_collection.json`

### 3. Test Frontend Connection
```javascript
// Add to your App.jsx or main component
useEffect(() => {
  fetch('http://localhost:5000/api/employees')
    .then(r => r.json())
    .then(data => console.log('API Connected:', data))
    .catch(err => console.error('API Connection Failed:', err))
}, [])
```

## Troubleshooting

### CORS Errors
**Problem:** `Access-Control-Allow-Origin` error

**Solution:** Check `.env` file in backend:
```env
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Backend Not Running
**Problem:** `Failed to fetch`

**Solution:**
```bash
cd backend
./run.sh  # Make sure backend is running
```

### Data Format Mismatch
**Problem:** Frontend expects `assignee` but gets `assignee_id`

**Solution:** Always use `?enrich=true` for tasks:
```javascript
api.getTasks()  // Already includes enrich=true
```

### Dates Not Parsing
**Problem:** Date format issues

**Solution:** Backend returns ISO format, parse with:
```javascript
new Date(task.dueDate).toLocaleDateString()
```

## Production Checklist

- [ ] Environment variables configured
- [ ] Database migrations applied
- [ ] CORS origins updated for production domain
- [ ] API base URL updated in frontend
- [ ] Error handling implemented
- [ ] Loading states added
- [ ] Authentication added (if needed)
- [ ] Rate limiting configured
- [ ] SSL/HTTPS enabled
- [ ] Database backups configured

## Next Steps

1. ✅ Migrate one component at a time
2. ✅ Test each component after migration
3. ✅ Keep mock data as fallback during migration
4. ✅ Remove mock data imports after successful migration
5. ✅ Add proper error handling
6. ✅ Implement loading states
7. ✅ Add authentication if needed

## Support

Need help? Check:
- `README.md` - Full API documentation
- `test_api.py` - Working examples of all endpoints
- Postman collection - Interactive API testing
