# projects.py
from flask import Blueprint, request, jsonify
# 'datetime' importlarını temizledim ve 'timedelta'yı doğrudan ekledim
from datetime import datetime, date, timedelta 
from models import Project, Task, Employee
from extensions import db
import random # Simülasyon için eklendi
# Yeni import'lar
import random 
import requests 
import json
import re 
projects_bp = Blueprint('projects', __name__, url_prefix='/api/projects')


# --- YENİ ENDPOINT: Yapay Zeka ile Görev Üretme ve Proje Oluşturma ---@projects_bp.route('/generate-tasks', methods=['POST'])
@projects_bp.route('/generate-tasks', methods=['POST'])
def generate_tasks_and_create_project():
    """
    Kullanıcıdan gelen proje detaylarını alır,
    LLM API’ye gönderir, gelen görevleri veritabanına işler.
    """
    # Gerekli import'ların yapıldığını varsayıyoruz:
    # from flask import request, jsonify, current_app
    # import random, requests, json
    # from datetime import date, timedelta, datetime
    # from your_models import Project, Task, Employee, db

    data = request.get_json()

    required_fields = ['project_title', 'metadata', 'team']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400

    project_title = data['project_title']
    project_id = f"p{random.randint(100, 999)}"
    while Project.query.get(project_id):
        project_id = f"p{random.randint(100, 999)}"

    if Project.query.filter_by(name=project_title).first():
        return jsonify({'error': 'Project name already exists.'}), 400

    # Ngrok URL veya sabit backend adresi
    AI_API_URL = "https://252b70dec01e.ngrok-free.app/api/generate"

    payload = {
        "json_input": data,
        "project_key": data.get("project_key", "INSIGHT"),
        "use_model": True
    }

    try:
        # --- LLM API’ye istek at ---
        response = requests.post(AI_API_URL, json=payload, timeout=120)
        response.raise_for_status()
        result = response.json()
        
        # --- LOGLAMA NOKTASI 1: LLM API'den Gelen Ham Cevap ---
        # Eğer flask uygulamanız varsa current_app.logger kullanın, yoksa print() veya logging modülü kullanın.
        print("--- LLM API Ham Cevabı ---")
        print(json.dumps(result, indent=2))
        print("--------------------------")


        if not result.get("success", True):
            return jsonify({'error': 'Model processing failed', 'details': result}), 500

        jira_json = result.get("jira_json")
        if not jira_json or "tasks" not in jira_json:
            return jsonify({'error': 'No tasks found in response.'}), 500

        tasks_from_llm = jira_json["tasks"]

    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Failed to reach AI API', 'details': str(e)}), 500

    # --- Proje oluştur ---
    due_date_obj = date.today() + timedelta(weeks=3)
    project = Project(
        project_id=project_id,
        name=project_title,
        description=data.get('metadata', {}).get('description', data.get('project_description', 'No description provided')),
        status='Planning',
        budget=data.get('budget', 0),
        priority='high',
        due_date=due_date_obj
    )
    db.session.add(project)

    # --- Görevleri veritabanına kaydet ---
    created_tasks = []

    for i, t in enumerate(tasks_from_llm):
        f = t["fields"]

        # Assignee bilgisi
        # Atanan kişi ID'sini çekmeye çalışırken kullanılan yol: f.get("assignee", {}).get("accountId")
        assignee_id = f.get("assignee", {}).get("accountId")
        
        # --- LOGLAMA NOKTASI 2: Her Görev İçin Atanan Kişi Verisi ---
        print(f"Task {i+1} Başlık: {f.get('summary')}")
        print(f"Task {i+1} 'assignee' alanı (tam): {f.get('assignee')}")
        print(f"Task {i+1} Çıkarılan assignee_id: {assignee_id}")
        print("--------------------------")


        # Estimated time (örnek: "4d" → saat cinsinden)
        estimate_str = f.get("timetracking", {}).get("originalEstimate", "0d")
        estimated_hours = 0
        if "d" in estimate_str:
            try:
                estimated_hours = int(estimate_str.replace("d", "")) * 8
            except:
                estimated_hours = 0

        # Task ID oluştur
        task_id = f"t{random.randint(100, 999)}"
        while Task.query.get(task_id):
            task_id = f"t{random.randint(100, 999)}"

        task = Task(
            task_id=task_id,
            title=f.get("summary"),
            # Description çekme mantığı karmaşık görünüyor, hata vermediği varsayılmıştır.
            description=f.get("description", {}).get("content", [{}])[0].get("content", [{}])[0].get("text", ""),
            estimated_hours=estimated_hours,
            priority=f.get("priority", {}).get("name", "Medium").lower(),
            status="Pending",
            # assignee_id, yukarıda LLM verisinden çekilen değerdir
            assignee_id=assignee_id, 
            project_id=project_id,
            due_date=datetime.strptime(f.get("duedate"), "%Y-%m-%d") if f.get("duedate") else None,
            created_at=datetime.utcnow()
        )

        db.session.add(task)
        created_tasks.append(task.to_dict())

        # Çalışanın yükünü güncelle
        if assignee_id:
            emp = Employee.query.get(assignee_id)
            if emp:
                emp.current_load_hours = (emp.current_load_hours or 0) + task.estimated_hours
            else:
                # --- EK LOGLAMA: Atanan ID Veritabanında Bulunamadı ---
                print(f"UYARI: {assignee_id} ID'li çalışan veritabanında bulunamadı!")
                print("--------------------------")

    db.session.commit()

    return jsonify({
        "message": "Project and tasks generated successfully from LLM response.",
        "project_id": project_id,
        "project": project.to_dict(),
        "generated_tasks": created_tasks
    }), 201
    
# --- Mevcut Proje CRUD ve Listeleme Fonksiyonları ---

@projects_bp.route('', methods=['GET'])
def get_projects():
    """Get all projects with optional filtering by status."""
    status = request.args.get('status')  # Filter by status
    include_tasks = request.args.get('include_tasks', 'false').lower() == 'true'
    
    query = Project.query
    
    if status:
        query = query.filter_by(status=status)
    
    projects = query.all()
    return jsonify([project.to_dict(include_tasks=include_tasks) for project in projects])

@projects_bp.route('/<project_id>', methods=['GET'])
def get_project(project_id):
    """Get a specific project by ID."""
    include_tasks = request.args.get('include_tasks', 'false').lower() == 'true'
    project = Project.query.get_or_404(project_id)
    
    result = project.to_dict(include_tasks=include_tasks)
    
    # Add team members (employees who have tasks in this project)
    if include_tasks or request.args.get('include_members', 'false').lower() == 'true':
        task_assignee_ids = [task.assignee_id for task in project.tasks if task.assignee_id]
        unique_assignee_ids = list(set(task_assignee_ids))
        # employee_id'lerin string olduğunu varsayıyoruz (e01, e02 gibi)
        members = Employee.query.filter(Employee.employee_id.in_(unique_assignee_ids)).all()
        result['members'] = [member.to_dict() for member in members]
    
    return jsonify(result)

@projects_bp.route('', methods=['POST'])
def create_project():
    """Create a new project (simple, without AI task generation)."""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['project_id', 'name', 'dueDate']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Check if project_id already exists
    if Project.query.get(data['project_id']):
        return jsonify({'error': 'Project ID already exists'}), 400
    
    # Check if project name already exists
    if Project.query.filter_by(name=data['name']).first():
        return jsonify({'error': 'Project name already exists'}), 400
    
    # Parse due_date
    try:
        # 'datetime' class'ı zaten import edildi, bu doğru
        due_date = datetime.strptime(data['dueDate'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    
    # Create new project
    project = Project(
        project_id=data['project_id'],
        name=data['name'],
        description=data.get('description', ''),
        status=data.get('status', 'Planning'),
        budget=data.get('budget', 0),
        priority=data.get('priority', 'medium'),
        due_date=due_date
    )
    
    db.session.add(project)
    db.session.commit()
    
    return jsonify(project.to_dict()), 201

@projects_bp.route('/<project_id>', methods=['PUT'])
def update_project(project_id):
    """Update an existing project."""
    project = Project.query.get_or_404(project_id)
    data = request.get_json()
    
    # Update fields
    if 'name' in data:
        # Check if new name already exists for a different project
        existing = Project.query.filter_by(name=data['name']).first()
        if existing and existing.project_id != project_id:
            return jsonify({'error': 'Project name already exists'}), 400
        project.name = data['name']
    
    if 'description' in data:
        project.description = data['description']
    
    if 'status' in data:
        project.status = data['status']
    
    if 'budget' in data:
        project.budget = data['budget']
    
    if 'priority' in data:
        project.priority = data['priority']
    
    if 'dueDate' in data:
        try:
            # 'datetime' class'ı zaten import edildi, bu doğru
            project.due_date = datetime.strptime(data['dueDate'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    
    db.session.commit()
    
    return jsonify(project.to_dict())

@projects_bp.route('/<project_id>', methods=['DELETE'])
def delete_project(project_id):
    """Delete a project (and all its tasks via cascade delete)."""
    project = Project.query.get_or_404(project_id)
    
    db.session.delete(project)
    db.session.commit()
    
    return '', 204

@projects_bp.route('/<project_id>/tasks', methods=['GET'])
def get_project_tasks(project_id):
    """Get all tasks for a specific project. Includes 'enrich=true' by default for frontend visibility."""
    # Proje ID'sinin varlığını kontrol et
    project = Project.query.get_or_404(project_id)
    
    # 'enrich' parametresini al. Frontend'in görevleri düzgün göstermesi için varsayılanı 'true' yaptık.
    enrich = request.args.get('enrich', 'true').lower() == 'true' 
    
    # Projenin tüm görevlerini getir
    tasks = [task.to_dict(enrich=enrich) for task in project.tasks]
    
    return jsonify(tasks)

@projects_bp.route('/<project_id>/members', methods=['GET'])
def get_project_members(project_id):
    """Get all team members working on a project."""
    project = Project.query.get_or_404(project_id)
    
    # Get unique assignee IDs from project tasks
    task_assignee_ids = [task.assignee_id for task in project.tasks if task.assignee_id]
    unique_assignee_ids = list(set(task_assignee_ids))
    
    # Get employee details
    members = Employee.query.filter(Employee.employee_id.in_(unique_assignee_ids)).all()
    
    return jsonify([member.to_dict() for member in members])

@projects_bp.route('/<project_id>/stats', methods=['GET'])
def get_project_stats(project_id):
    """Get project statistics based on its tasks."""
    project = Project.query.get_or_404(project_id)
    
    tasks = project.tasks
    total_tasks = len(tasks)
    
    stats = {
        'project': project.to_dict(),
        'tasks': {
            'total': total_tasks,
            'completed': len([t for t in tasks if t.status == 'Completed']),
            'in_progress': len([t for t in tasks if t.status == 'In Progress']),
            'pending': len([t for t in tasks if t.status == 'Pending']),
            'blocked': len([t for t in tasks if t.status == 'Blocked'])
        },
        'priority': {
            'critical': len([t for t in tasks if t.priority == 'critical']),
            'high': len([t for t in tasks if t.priority == 'high']),
            'medium': len([t for t in tasks if t.priority == 'medium']),
            'low': len([t for t in tasks if t.priority == 'low'])
        },
        'estimated_hours': {
            'total': sum(t.estimated_hours for t in tasks),
            'completed': sum(t.estimated_hours for t in tasks if t.status == 'Completed'),
            'remaining': sum(t.estimated_hours for t in tasks if t.status != 'Completed')
        }
    }
    
    return jsonify(stats)