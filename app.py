print("Git push test")
import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "alphanex-demo-secret-key-for-session-management-2025")
app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF globally for better compatibility
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database - use PostgreSQL for production and multi-user support
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///alphanex.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
    "pool_timeout": 20,
    "pool_size": 10,
    "max_overflow": 20
}

# Configure upload settings
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Initialize extensions with error handling
try:
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    # login_manager.login_view = 'name_entry'  # Disabled for demo mode
    login_manager.login_message = ""  # Empty string instead of None
    login_manager.session_protection = "strong"
except Exception as e:
    app.logger.error(f"Extension initialization failed: {e}")
    # Create minimal fallback login manager
    login_manager = LoginManager()
    login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    try:
        from models import User
        return User.query.get(int(user_id))
    except Exception as e:
        app.logger.error(f"User loading failed: {e}")
        return None


# Create upload directory with error handling
try:
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
except Exception as e:
    app.logger.error(f"Upload directory creation failed: {e}")
    # Fallback to temp directory
    import tempfile
    app.config['UPLOAD_FOLDER'] = tempfile.mkdtemp()

# Initialize scheduler for automated tasks with error handling
try:
    scheduler = BackgroundScheduler()
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())
except Exception as e:
    app.logger.error(f"Scheduler initialization failed: {e}")
    # Continue without scheduler - not critical for basic functionality

with app.app_context():
    # Import models to ensure tables are created
    import models  # noqa: F401
    import routes  # noqa: F401

    try:
        db.create_all()
    except Exception as e:
        app.logger.error(f"Database initialization error: {e}")
        # Continue running even if DB init fails

# Comprehensive error handlers to prevent crashes
@app.errorhandler(404)
def not_found(e):
    app.logger.warning(f"404 error: {e}")
    try:
        from flask import render_template
        return render_template('404.html'), 404
    except:
        return "Page not found. <a href='/'>Return to homepage</a>", 404

@app.errorhandler(500)
def internal_server_error(e):
    app.logger.error(f"Internal server error: {e}")
    try:
        from flask import render_template
        return render_template('500.html'), 500
    except:
        return "Internal server error occurred. <a href='/'>Return to homepage</a>", 500

@app.errorhandler(502)
def bad_gateway(e):
    app.logger.error(f"Bad gateway error: {e}")
    return "Service temporarily unavailable. <a href='/'>Return to homepage</a>", 502

@app.errorhandler(413)
def request_entity_too_large(e):
    app.logger.warning(f"File too large: {e}")
    return "File too large. Maximum file size is 100MB. <a href='/upload'>Try again</a>", 413

@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f"Unhandled exception: {e}")
    import traceback
    app.logger.error(f"Traceback: {traceback.format_exc()}")
    try:
        from flask import render_template
        return render_template('error.html', error=str(e)), 500
    except:
        return f"An unexpected error occurred: {str(e)}. <a href='/'>Return to homepage</a>", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
