from flask import Blueprint, request, jsonify
from models import Employee
from extensions import db

employees_bp = Blueprint('employees', __name__, url_prefix='/api/employees')

@employees_bp.route('', methods=['GET'])
def get_employees():
    """Get all employees"""
    role = request.args.get('role')  # Filter by user_role (pm or executor)
    
    query = Employee.query
    
    if role:
        query = query.filter_by(user_role=role)
    
    employees = query.all()
    return jsonify([emp.to_dict() for emp in employees])

@employees_bp.route('/<employee_id>', methods=['GET'])
def get_employee(employee_id):
    """Get a specific employee"""
    employee = Employee.query.get_or_404(employee_id)
    return jsonify(employee.to_dict())

@employees_bp.route('', methods=['POST'])
def create_employee():
    """Create a new employee"""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['employee_id', 'name', 'role', 'user_role', 'avatar']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Check if employee_id already exists
    if Employee.query.get(data['employee_id']):
        return jsonify({'error': 'Employee ID already exists'}), 400
    
    # Create new employee
    employee = Employee(
        employee_id=data['employee_id'],
        name=data['name'],
        role=data['role'],
        user_role=data['user_role'],
        avatar=data['avatar'],
        capacity_hours_per_week=data.get('capacity_hours_per_week', 40),
        current_load_hours=data.get('current_load_hours', 0),
        integrations=data.get('integrations', {}),
        languages=data.get('languages', []),
        skills=data.get('skills', []),
        timezone=data.get('timezone', 'UTC')
    )
    
    db.session.add(employee)
    db.session.commit()
    
    return jsonify(employee.to_dict()), 201

@employees_bp.route('/<employee_id>', methods=['PUT'])
def update_employee(employee_id):
    """Update an employee"""
    employee = Employee.query.get_or_404(employee_id)
    data = request.get_json()
    
    # Update fields
    allowed_fields = ['name', 'role', 'user_role', 'avatar', 'capacity_hours_per_week', 
                     'current_load_hours', 'integrations', 'languages', 'skills', 'timezone']
    
    for field in allowed_fields:
        if field in data:
            setattr(employee, field, data[field])
    
    db.session.commit()
    
    return jsonify(employee.to_dict())

@employees_bp.route('/<employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    """Delete an employee"""
    employee = Employee.query.get_or_404(employee_id)
    
    # Check if employee has assigned tasks
    if employee.assigned_tasks:
        return jsonify({'error': 'Cannot delete employee with assigned tasks'}), 400
    
    db.session.delete(employee)
    db.session.commit()
    
    return '', 204

@employees_bp.route('/<employee_id>/workload', methods=['GET'])
def get_employee_workload(employee_id):
    """Get employee's workload information"""
    employee = Employee.query.get_or_404(employee_id)
    
    # Calculate workload from tasks
    from models import Task
    assigned_tasks = Task.query.filter_by(assignee_id=employee_id).all()
    
    total_estimated_hours = sum(task.estimated_hours for task in assigned_tasks if task.status != 'Completed')
    in_progress_count = len([t for t in assigned_tasks if t.status == 'In Progress'])
    pending_count = len([t for t in assigned_tasks if t.status == 'Pending'])
    completed_count = len([t for t in assigned_tasks if t.status == 'Completed'])
    
    return jsonify({
        'employee': employee.to_dict(),
        'workload': {
            'current_load_hours': employee.current_load_hours,
            'capacity_hours_per_week': employee.capacity_hours_per_week,
            'available_hours': employee.capacity_hours_per_week - employee.current_load_hours,
            'utilization_percentage': round((employee.current_load_hours / employee.capacity_hours_per_week * 100), 2),
            'total_estimated_hours': total_estimated_hours,
            'in_progress_tasks': in_progress_count,
            'pending_tasks': pending_count,
            'completed_tasks': completed_count
        }
    })
