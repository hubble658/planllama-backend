from datetime import datetime
from sqlalchemy import JSON
from extensions import db

class Employee(db.Model):
    """Employee model - represents both PMs and Executors"""
    __tablename__ = 'employees'
    
    employee_id = db.Column(db.String(10), primary_key=True)  # e.g., 'e01'
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)  # e.g., 'Backend Engineer', 'Project Manager'
    user_role = db.Column(db.String(20), nullable=False)  # 'pm' or 'executor'
    avatar = db.Column(db.String(10), nullable=False)  # e.g., 'MC'
    capacity_hours_per_week = db.Column(db.Integer, default=40)
    current_load_hours = db.Column(db.Integer, default=0)
    
    # JSON fields
    integrations = db.Column(JSON, default=dict)  # email, jira_account_id, slack_user_id
    languages = db.Column(JSON, default=list)  # ['en', 'tr']
    skills = db.Column(JSON, default=list)  # [{'name': 'python', 'level': 5}]
    
    timezone = db.Column(db.String(50), default='UTC')
    
    # Relationships
    assigned_tasks = db.relationship('Task', back_populates='assignee', foreign_keys='Task.assignee_id')
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            'employee_id': self.employee_id,
            'name': self.name,
            'role': self.role,
            'user_role': self.user_role,
            'avatar': self.avatar,
            'capacity_hours_per_week': self.capacity_hours_per_week,
            'current_load_hours': self.current_load_hours,
            'integrations': self.integrations or {},
            'languages': self.languages or [],
            'skills': self.skills or [],
            'timezone': self.timezone,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Project(db.Model):
    """Project model"""
    __tablename__ = 'projects'
    
    project_id = db.Column(db.String(10), primary_key=True)  # e.g., 'p01'
    name = db.Column(db.String(200), nullable=False, unique=True)
    description = db.Column(db.Text)
    status = db.Column(db.String(50), default='Planning')  # Planning, In Progress, On Hold, Completed
    budget = db.Column(db.Integer, default=0)
    priority = db.Column(db.String(20), default='medium')  # low, medium, high, critical
    
    # Dates
    due_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    tasks = db.relationship('Task', back_populates='project', cascade='all, delete-orphan')
    
    def to_dict(self, include_tasks=False):
        """Convert model to dictionary"""
        # Calculate task counts
        tasks_count = len(self.tasks)
        completed_tasks = len([t for t in self.tasks if t.status == 'Completed'])
        
        result = {
            'project_id': self.project_id,
            'name': self.name,
            'description': self.description,
            'status': self.status,
            'budget': self.budget,
            'priority': self.priority,
            'dueDate': self.due_date.isoformat() if self.due_date else None,
            'createdAt': self.created_at.date().isoformat() if self.created_at else None,
            'tasksCount': tasks_count,
            'completedTasks': completed_tasks
        }
        
        if include_tasks:
            result['tasks'] = [task.to_dict() for task in self.tasks]
        
        return result


class Task(db.Model):
    """Task model"""
    __tablename__ = 'tasks'
    
    task_id = db.Column(db.String(10), primary_key=True)  # e.g., 't01'
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(50), default='Pending')  # Pending, In Progress, Completed, Blocked
    priority = db.Column(db.String(20), default='medium')  # low, medium, high, critical
    
    # Foreign keys
    assignee_id = db.Column(db.String(10), db.ForeignKey('employees.employee_id'), nullable=True)
    project_id = db.Column(db.String(10), db.ForeignKey('projects.project_id'), nullable=False)
    
    # Task details
    estimated_hours = db.Column(db.Float, default=0)
    
    # Dates
    due_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    assignee = db.relationship('Employee', back_populates='assigned_tasks', foreign_keys=[assignee_id])
    project = db.relationship('Project', back_populates='tasks')
    
    def to_dict(self, enrich=False):
        """Convert model to dictionary
        
        Args:
            enrich: If True, include assignee name and project name
        """
        result = {
            'task_id': self.task_id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'assignee_id': self.assignee_id,
            'project_id': self.project_id,
            'estimatedHours': self.estimated_hours,
            'dueDate': self.due_date.isoformat() if self.due_date else None,
            'createdAt': self.created_at.date().isoformat() if self.created_at else None,
            'completedAt': self.completed_at.isoformat() if self.completed_at else None
        }
        
        # Add enriched data (for frontend compatibility)
        if enrich:
            result['assignee'] = self.assignee.name if self.assignee else 'Unassigned'
            result['project'] = self.project.name if self.project else 'Unknown Project'
        
        return result
