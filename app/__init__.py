from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')

    # Inicjalizacja rozszerzeń
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    migrate = Migrate(app, db)

    login_manager.login_view = 'auth.login'

    # Import modeli
    from app.models import Uzytkownik

    # Rejestracja blueprintów
    from app.auth.routes import auth as auth_blueprint
    from app.routes import main as main_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)

    # Ładowanie użytkownika
    @login_manager.user_loader
    def load_user(user_id):
        return Uzytkownik.query.get(int(user_id))

    return app
