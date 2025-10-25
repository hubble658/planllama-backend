from flask import Blueprint, request, jsonify
from datetime import datetime, date
from models import Task, Project, Employee
from extensions import db

tasks_bp = Blueprint('tasks', __name__, url_prefix='/api/tasks')

def parse_date_string(date_str):
    """Gelen YYYY-MM-DD string'ini Python date objesine çevirir."""
    if not date_str:
        return None
    if isinstance(date_str, date):
        return date_str
    try:
        # Sadece tarihi ayrıştırmak için .date() metodunu kullanıyoruz
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return None # Hatalı format gelirse None dön

@tasks_bp.route('', methods=['GET'])
def get_tasks():
    """Get all tasks with optional filtering"""
    # Query parameters
    status = request.args.get('status')
    priority = request.args.get('priority')
    assignee_id = request.args.get('assignee_id')
    project_id = request.args.get('project_id')
    enrich = request.args.get('enrich', 'true').lower() == 'true'
    
    query = Task.query
    
    # Apply filters
    if status:
        query = query.filter_by(status=status)
    if priority:
        query = query.filter_by(priority=priority)
    if assignee_id:
        query = query.filter_by(assignee_id=assignee_id)
    if project_id:
        query = query.filter_by(project_id=project_id)
    
    tasks = query.all()
    return jsonify([task.to_dict(enrich=enrich) for task in tasks])

@tasks_bp.route('/<task_id>', methods=['GET'])
def get_task(task_id):
    """Get a specific task"""
    enrich = request.args.get('enrich', 'true').lower() == 'true'
    task = Task.query.get_or_404(task_id)
    return jsonify(task.to_dict(enrich=enrich))

@tasks_bp.route('', methods=['POST'])
def create_task():
    """Create a new task"""
    data = request.json
    
    # Due Date Ayrıştırma: SQLite'ın beklediği Python date objesine çevir
    due_date_obj = parse_date_string(data.get('due_date'))
    
    # Zorunlu alan kontrolü (NOT NULL constraint'i için)
    if not due_date_obj:
        return jsonify({'error': 'Missing or invalid date format for due_date. Use YYYY-MM-DD'}), 400
    
    # Yeni task oluştur
    task = Task(
        task_id=data.get('task_id') or f"t{int(datetime.utcnow().timestamp())}",
        title=data.get('title'),
        description=data.get('description'),
        status=data.get('status', 'Pending'),
        priority=data.get('priority', 'medium'),
        assignee_id=data.get('assignee_id'),
        project_id=data.get('project_id'),
        estimated_hours=data.get('estimated_hours', 0),
        due_date=due_date_obj, # Ayrıştırılmış date objesi kullanılıyor
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    # Assignee varsa ve status completed değilse workload'a ekle
    if task.assignee_id and task.status != 'Completed':
        employee = Employee.query.get(task.assignee_id)
        if employee:
            employee.current_load_hours = employee.current_load_hours + (task.estimated_hours or 0)
    
    db.session.add(task)
    db.session.commit()
    
    return jsonify(task.to_dict()), 201


@tasks_bp.route('/<task_id>', methods=['PUT'])
def update_task(task_id):
    """Update a task"""
    task = Task.query.get_or_404(task_id)
    data = request.json
    
    old_assignee_id = task.assignee_id
    old_estimated_hours = task.estimated_hours or 0
    old_status = task.status
    
    new_assignee_id = data.get('assignee_id', task.assignee_id)
    new_estimated_hours = data.get('estimated_hours', task.estimated_hours) or 0
    new_status = data.get('status', task.status)
    
    # Workload hesaplaması - sadece completed olmayan task'lar için
    if old_status != 'Completed' and new_status != 'Completed':
        # Assignee veya estimated_hours değiştiyse
        if old_assignee_id != new_assignee_id or old_estimated_hours != new_estimated_hours:
            # Eski assignee'den çıkar
            if old_assignee_id:
                old_employee = Employee.query.get(old_assignee_id)
                if old_employee:
                    old_employee.current_load_hours = max(0, old_employee.current_load_hours - old_estimated_hours)
            
            # Yeni assignee'ye ekle
            if new_assignee_id:
                new_employee = Employee.query.get(new_assignee_id)
                if new_employee:
                    new_employee.current_load_hours = new_employee.current_load_hours + new_estimated_hours
    
    # Status değişimi kontrolü
    if old_status != new_status:
        if new_status == 'Completed' and old_status != 'Completed':
            # Completed'a geçiş - workload'dan çıkar
            if new_assignee_id:
                employee = Employee.query.get(new_assignee_id)
                if employee:
                    employee.current_load_hours = max(0, employee.current_load_hours - new_estimated_hours)
        
        elif old_status == 'Completed' and new_status != 'Completed':
            # Completed'dan çıkış - workload'a ekle
            if new_assignee_id:
                employee = Employee.query.get(new_assignee_id)
                if employee:
                    employee.current_load_hours = employee.current_load_hours + new_estimated_hours
    
    # Task'ı güncelle
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.status = new_status
    task.priority = data.get('priority', task.priority)
    task.assignee_id = new_assignee_id
    task.project_id = data.get('project_id', task.project_id)
    task.estimated_hours = new_estimated_hours
    
    # Due Date'i güncelle ve ayrıştır
    if 'due_date' in data:
        new_due_date = parse_date_string(data['due_date'])
        if not new_due_date:
            return jsonify({'error': 'Invalid date format for due_date. Use YYYY-MM-DD'}), 400
        task.due_date = new_due_date
        
    task.updated_at = datetime.utcnow()
    
    if new_status == 'Completed':
        task.completed_at = datetime.utcnow()
    else:
        task.completed_at = None
    
    db.session.commit()
    
    return jsonify(task.to_dict()), 200

@tasks_bp.route('/<task_id>/status', methods=['PATCH'])
def update_task_status(task_id):
    """Update task status"""
    task = Task.query.get_or_404(task_id)
    data = request.json
    new_status = data.get('status')
    
    if not new_status:
        return jsonify({'error': 'Status is required'}), 400
    
    old_status = task.status
    
    # Status değiştiğinde workload güncelle
    if task.assignee_id and old_status != new_status:
        employee = Employee.query.get(task.assignee_id)
        
        if employee:
            # Eğer completed'a geçtiyse, workload'dan çıkar
            if new_status == 'Completed' and old_status != 'Completed':
                employee.current_load_hours = max(0, employee.current_load_hours - (task.estimated_hours or 0))
            
            # Eğer completed'dan başka bir status'a geçtiyse, workload'a ekle
            elif old_status == 'Completed' and new_status != 'Completed':
                employee.current_load_hours = employee.current_load_hours + (task.estimated_hours or 0)
    
    task.status = new_status
    task.updated_at = datetime.utcnow()
    
    if new_status == 'Completed':
        task.completed_at = datetime.utcnow()
    else:
        task.completed_at = None
    
    db.session.commit()
    
    return jsonify(task.to_dict()), 200

@tasks_bp.route('/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task"""
    task = Task.query.get_or_404(task_id)
    
    # Task silinmeden önce assignee'nin workload'unu güncelle
    # Sadece completed olmayan task'lar workload'dan çıkarılır
    if task.assignee_id and task.status != 'Completed':
        employee = Employee.query.get(task.assignee_id)
        if employee:
            employee.current_load_hours = max(0, employee.current_load_hours - (task.estimated_hours or 0))
    
    db.session.delete(task)
    db.session.commit()
    return '', 204

@tasks_bp.route('/by-assignee/<assignee_id>', methods=['GET'])
def get_tasks_by_assignee(assignee_id):
    """Get all tasks assigned to a specific employee"""
    # Verify employee exists
    employee = Employee.query.get_or_404(assignee_id)
    
    enrich = request.args.get('enrich', 'true').lower() == 'true'
    status = request.args.get('status')
    
    query = Task.query.filter_by(assignee_id=assignee_id)
    
    if status:
        query = query.filter_by(status=status)
    
    tasks = query.all()
    
    return jsonify({
        'employee': employee.to_dict(),
        'tasks': [task.to_dict(enrich=enrich) for task in tasks]
    })

@tasks_bp.route('/by-project/<project_id>', methods=['GET'])
def get_tasks_by_project(project_id):
    """Get all tasks for a specific project"""
    # Verify project exists
    project = Project.query.get_or_404(project_id)
    
    enrich = request.args.get('enrich', 'true').lower() == 'true'
    status = request.args.get('status')
    
    query = Task.query.filter_by(project_id=project_id)
    
    if status:
        query = query.filter_by(status=status)
    
    tasks = query.all()
    
    return jsonify({
        'project': project.to_dict(),
        'tasks': [task.to_dict(enrich=enrich) for task in tasks]
    })

@tasks_bp.route('/stats', methods=['GET'])
def get_tasks_stats():
    """Get overall task statistics"""
    all_tasks = Task.query.all()
    
    stats = {
        'total': len(all_tasks),
        'by_status': {
            'pending': len([t for t in all_tasks if t.status == 'Pending']),
            'in_progress': len([t for t in all_tasks if t.status == 'In Progress']),
            'completed': len([t for t in all_tasks if t.status == 'Completed']),
            'blocked': len([t for t in all_tasks if t.status == 'Blocked'])
        },
        'by_priority': {
            'critical': len([t for t in all_tasks if t.priority == 'critical']),
            'high': len([t for t in all_tasks if t.priority == 'high']),
            'medium': len([t for t in all_tasks if t.priority == 'medium']),
            'low': len([t for t in all_tasks if t.priority == 'low'])
        },
        'estimated_hours': {
            'total': sum(t.estimated_hours for t in all_tasks),
            'completed': sum(t.estimated_hours for t in all_tasks if t.status == 'Completed'),
            'remaining': sum(t.estimated_hours for t in all_tasks if t.status != 'Completed')
        }
    }
    
    return jsonify(stats)
