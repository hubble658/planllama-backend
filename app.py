import os
from flask import Flask, jsonify
from config import config
from extensions import db, migrate, cors
from models import Employee, Project, Task

def create_app(config_name=None):
    """Application factory pattern"""
    
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app, resources={
        r"/api/*": {
            "origins": app.config['CORS_ORIGINS'],
            "methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Register blueprints
    from routes.employees import employees_bp
    from routes.projects import projects_bp
    from routes.tasks import tasks_bp
    
    app.register_blueprint(employees_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(tasks_bp)
    
    # Root endpoint
    @app.route('/')
    def index():
        return jsonify({
            'message': 'PlanLLaMA API',
            'version': '1.0.0',
            'endpoints': {
                'employees': '/api/employees',
                'projects': '/api/projects',
                'tasks': '/api/tasks'
            }
        })
    
    # Health check endpoint
    @app.route('/health')
    def health():
        return jsonify({'status': 'healthy'})
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500
    
    # Shell context for flask shell
    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'Employee': Employee,
            'Project': Project,
            'Task': Task
        }
    
    return app

# Create app instance
app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'True') == 'True'
    app.run(host='0.0.0.0', port=port, debug=debug)
