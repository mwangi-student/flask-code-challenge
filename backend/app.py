from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from datetime import timedelta
from models import db, TokenBlocklist
from flask_mail import Mail
from views.user import user_bp
from views.house import house_bp
from views.auth import auth_bp

# Initialize the Mail instance here, but we won't bind it to the app until inside create_app
mail = Mail()

def create_app():
    app = Flask(__name__)

    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///house.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # JWT configuration
    app.config["JWT_SECRET_KEY"] = "jyuvtycuiiuyctrxtrgvtyvuiuytdf"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

    # Flask-Mail configuration
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = 'mwangi.brian@student.moringaschool.com'
    app.config['MAIL_PASSWORD'] = 'kqsq xrws pkwz dpyb'
    app.config['MAIL_DEFAULT_SENDER'] = 'mwangi.brian@student.moringaschool.com'

    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)
    mail.init_app(app)

    # Register blueprints
    app.register_blueprint(user_bp)
    app.register_blueprint(house_bp)
    app.register_blueprint(auth_bp)

    # JWT blocklist check
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
        jti = jwt_payload["jti"]
        token_exists = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
        return token_exists is not None

    return app
