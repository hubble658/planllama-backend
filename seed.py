from datetime import datetime, date
from extensions import db
from models import Employee, Project, Task

def seed_database():
    """Seed the database with initial data matching the frontend mock data"""
    print("Seeding database...")
    # Clear existing data
    db.session.query(Task).delete()
    db.session.query(Project).delete()
    db.session.query(Employee).delete()
    
    # Seed Employees
    employees_data = [
        {
            'employee_id': 'e01',
            'name': 'Sarah Johnson',
            'role': 'Project Manager',
            'user_role': 'pm',
            'avatar': 'SJ',
            'capacity_hours_per_week': 40,
            'current_load_hours': 32,
            'integrations': {
                'email': 'sarah.johnson@codelllama.ai',
                'jira_account_id': '5f9c-e01',
                'slack_user_id': 'U01ABC'
            },
            'languages': ['en', 'es'],
            'skills': [
                {'name': 'project_management', 'level': 5},
                {'name': 'agile', 'level': 5},
                {'name': 'leadership', 'level': 4},
                {'name': 'stakeholder_management', 'level': 4}
            ],
            'timezone': 'America/New_York'
        },
        {
            'employee_id': 'e02',
            'name': 'David Wilson',
            'role': 'Senior Project Manager',
            'user_role': 'pm',
            'avatar': 'DW',
            'capacity_hours_per_week': 40,
            'current_load_hours': 28,
            'integrations': {
                'email': 'david.wilson@codelllama.ai',
                'jira_account_id': '5f9c-e02',
                'slack_user_id': 'U02DEF'
            },
            'languages': ['en', 'fr'],
            'skills': [
                {'name': 'project_management', 'level': 5},
                {'name': 'scrum', 'level': 5},
                {'name': 'risk_management', 'level': 5},
                {'name': 'budgeting', 'level': 4}
            ],
            'timezone': 'America/Los_Angeles'
        },
        {
            'employee_id': 'e03',
            'name': 'Michael Chen',
            'role': 'Backend Engineer',
            'user_role': 'executor',
            'avatar': 'MC',
            'capacity_hours_per_week': 40,
            'current_load_hours': 35,
            'integrations': {
                'email': 'michael.chen@codelllama.ai',
                'jira_account_id': '5f9c-e03',
                'slack_user_id': 'U03GHI'
            },
            'languages': ['en', 'zh'],
            'skills': [
                {'name': 'python', 'level': 5},
                {'name': 'fastapi', 'level': 5},
                {'name': 'postgresql', 'level': 4},
                {'name': 'redis', 'level': 4},
                {'name': 'docker', 'level': 4}
            ],
            'timezone': 'Asia/Shanghai'
        },
        {
            'employee_id': 'e04',
            'name': 'Emily Davis',
            'role': 'UI/UX Designer',
            'user_role': 'executor',
            'avatar': 'ED',
            'capacity_hours_per_week': 40,
            'current_load_hours': 22,
            'integrations': {
                'email': 'emily.davis@codelllama.ai',
                'jira_account_id': '5f9c-e04',
                'slack_user_id': 'U04JKL'
            },
            'languages': ['en', 'de'],
            'skills': [
                {'name': 'figma', 'level': 5},
                {'name': 'ui_design', 'level': 5},
                {'name': 'ux_research', 'level': 4},
                {'name': 'prototyping', 'level': 4},
                {'name': 'user_testing', 'level': 3}
            ],
            'timezone': 'Europe/Berlin'
        },
        {
            'employee_id': 'e05',
            'name': 'Alex Kumar',
            'role': 'Frontend Developer',
            'user_role': 'executor',
            'avatar': 'AK',
            'capacity_hours_per_week': 40,
            'current_load_hours': 30,
            'integrations': {
                'email': 'alex.kumar@codelllama.ai',
                'jira_account_id': '5f9c-e05',
                'slack_user_id': 'U05MNO'
            },
            'languages': ['en', 'hi'],
            'skills': [
                {'name': 'react', 'level': 5},
                {'name': 'typescript', 'level': 5},
                {'name': 'tailwind', 'level': 4},
                {'name': 'nextjs', 'level': 4},
                {'name': 'graphql', 'level': 3}
            ],
            'timezone': 'Asia/Kolkata'
        },
        {
            'employee_id': 'e06',
            'name': 'Yavuz Kaya',
            'role': 'Backend Engineer',
            'user_role': 'executor',
            'avatar': 'YK',
            'capacity_hours_per_week': 40,
            'current_load_hours': 18,
            'integrations': {
                'email': 'yavuz.k@codelllama.ai',
                'jira_account_id': '5f9c-e06',
                'slack_user_id': 'U06PQR'
            },
            'languages': ['tr', 'en'],
            'skills': [
                {'name': 'python', 'level': 5},
                {'name': 'fastapi', 'level': 5},
                {'name': 'redis', 'level': 4},
                {'name': 'mongodb', 'level': 4},
                {'name': 'aws', 'level': 3}
            ],
            'timezone': 'Europe/Istanbul'
        }
    ]
    
    for emp_data in employees_data:
        employee = Employee(**emp_data)
        db.session.add(employee)
    
    print(f"Added {len(employees_data)} employees")
    
    # Seed Projects
    projects_data = [
        {
            'project_id': 'p01',
            'name': 'Website Redesign',
            'description': 'Complete redesign of company website',
            'status': 'In Progress',
            'due_date': date(2025, 11, 15),
            'budget': 50000,
            'priority': 'high'
        },
        {
            'project_id': 'p02',
            'name': 'Mobile App Development',
            'description': 'Build iOS and Android mobile application',
            'status': 'In Progress',
            'due_date': date(2025, 12, 1),
            'budget': 100000,
            'priority': 'critical'
        },
        {
            'project_id': 'p03',
            'name': 'API Integration',
            'description': 'Integrate third-party APIs',
            'status': 'In Progress',
            'due_date': date(2025, 11, 30),
            'budget': 30000,
            'priority': 'medium'
        },
        {
            'project_id': 'p04',
            'name': 'E-commerce Platform',
            'description': 'Build complete e-commerce solution with payment integration',
            'status': 'In Progress',
            'due_date': date(2025, 12, 15),
            'budget': 150000,
            'priority': 'critical'
        },
        {
            'project_id': 'p05',
            'name': 'DevOps',
            'description': 'Setup CI/CD pipeline and infrastructure automation',
            'status': 'In Progress',
            'due_date': date(2025, 11, 20),
            'budget': 40000,
            'priority': 'high'
        }
    ]
    
    for proj_data in projects_data:
        project = Project(**proj_data)
        db.session.add(project)
    
    print(f"Added {len(projects_data)} projects")
    
    # Seed Tasks
    tasks_data = [
        {
            'task_id': 't01',
            'title': 'Design homepage mockup',
            'description': 'Create high-fidelity mockup for the new homepage',
            'status': 'In Progress',
            'priority': 'high',
            'assignee_id': 'e04',
            'project_id': 'p01',
            'due_date': date(2025, 10, 28),
            'estimated_hours': 8
        },
        {
            'task_id': 't02',
            'title': 'Implement user authentication',
            'description': 'Set up JWT-based authentication system',
            'status': 'Pending',
            'priority': 'critical',
            'assignee_id': 'e03',
            'project_id': 'p02',
            'due_date': date(2025, 10, 30),
            'estimated_hours': 16
        },
        {
            'task_id': 't03',
            'title': 'Write API documentation',
            'description': 'Document all REST API endpoints',
            'status': 'In Progress',
            'priority': 'medium',
            'assignee_id': 'e03',
            'project_id': 'p03',
            'due_date': date(2025, 11, 5),
            'estimated_hours': 12
        },
        {
            'task_id': 't04',
            'title': 'Setup database schema',
            'description': 'Design and implement database tables',
            'status': 'Completed',
            'priority': 'high',
            'assignee_id': 'e03',
            'project_id': 'p02',
            'due_date': date(2025, 10, 20),
            'estimated_hours': 10,
            'completed_at': datetime(2025, 10, 19)
        },
        {
            'task_id': 't05',
            'title': 'Create component library',
            'description': 'Build reusable React components',
            'status': 'Pending',
            'priority': 'low',
            'assignee_id': 'e04',
            'project_id': 'p01',
            'due_date': date(2025, 11, 10),
            'estimated_hours': 20
        },
        {
            'task_id': 't06',
            'title': 'Implement payment gateway',
            'description': 'Integrate Stripe payment system',
            'status': 'In Progress',
            'priority': 'critical',
            'assignee_id': 'e03',
            'project_id': 'p04',
            'due_date': date(2025, 11, 1),
            'estimated_hours': 24
        },
        {
            'task_id': 't07',
            'title': 'Design product cards',
            'description': 'Create responsive product card components',
            'status': 'Completed',
            'priority': 'medium',
            'assignee_id': 'e04',
            'project_id': 'p04',
            'due_date': date(2025, 10, 22),
            'estimated_hours': 6,
            'completed_at': datetime(2025, 10, 21)
        },
        {
            'task_id': 't08',
            'title': 'Setup CI/CD pipeline',
            'description': 'Configure GitHub Actions for automated deployment',
            'status': 'In Progress',
            'priority': 'high',
            'assignee_id': 'e03',
            'project_id': 'p05',
            'due_date': date(2025, 11, 3),
            'estimated_hours': 8
        },
        {
            'task_id': 't09',
            'title': 'Create landing page',
            'description': 'Design and implement marketing landing page',
            'status': 'Pending',
            'priority': 'medium',
            'assignee_id': 'e04',
            'project_id': 'p01',
            'due_date': date(2025, 11, 8),
            'estimated_hours': 12
        },
        {
            'task_id': 't10',
            'title': 'Implement push notifications',
            'description': 'Add Firebase push notifications to mobile app',
            'status': 'Pending',
            'priority': 'high',
            'assignee_id': 'e03',
            'project_id': 'p02',
            'due_date': date(2025, 11, 12),
            'estimated_hours': 16
        },
        {
            'task_id': 't11',
            'title': 'Create REST API endpoints',
            'description': 'Build user management API endpoints',
            'status': 'In Progress',
            'priority': 'critical',
            'assignee_id': 'e03',
            'project_id': 'p03',
            'due_date': date(2025, 10, 29),
            'estimated_hours': 14
        },
        {
            'task_id': 't12',
            'title': 'Design mobile UI screens',
            'description': 'Create UI mockups for all mobile app screens',
            'status': 'Completed',
            'priority': 'high',
            'assignee_id': 'e04',
            'project_id': 'p02',
            'due_date': date(2025, 10, 18),
            'estimated_hours': 20,
            'completed_at': datetime(2025, 10, 17)
        },
        {
            'task_id': 't13',
            'title': 'Implement search functionality',
            'description': 'Add Elasticsearch integration for product search',
            'status': 'Pending',
            'priority': 'medium',
            'assignee_id': 'e03',
            'project_id': 'p04',
            'due_date': date(2025, 11, 15),
            'estimated_hours': 18
        },
        {
            'task_id': 't14',
            'title': 'Create email templates',
            'description': 'Design responsive email templates for notifications',
            'status': 'In Progress',
            'priority': 'low',
            'assignee_id': 'e04',
            'project_id': 'p05',
            'due_date': date(2025, 11, 7),
            'estimated_hours': 8
        },
        {
            'task_id': 't15',
            'title': 'Performance optimization',
            'description': 'Optimize API response times and database queries',
            'status': 'Pending',
            'priority': 'high',
            'assignee_id': 'e03',
            'project_id': 'p03',
            'due_date': date(2025, 11, 20),
            'estimated_hours': 16
        }
    ]
    
    for task_data in tasks_data:
        task = Task(**task_data)
        db.session.add(task)
    
    print(f"Added {len(tasks_data)} tasks")
    
    # Commit all changes
    db.session.commit()
    
    print("Database seeded successfully!")
