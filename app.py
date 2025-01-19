from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from datetime import timedelta
from models import db, TokenBlocklist
from views.user import user_bp
from views.house import house_bp
from views.auth import auth_bp
app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///house.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
migrate = Migrate(app, db)
db.init_app(app)

# JWT configuration
app.config["JWT_SECRET_KEY"] = "jyuvtycuiiuyctrxtrgvtyvuiuytdf"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt = JWTManager(app)

# Blueprint registration
app.register_blueprint(user_bp)
app.register_blueprint(house_bp)
app.register_blueprint(auth_bp)

# JWT blocklist check
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    token_exists = db.session.query(TokenBlocklist.id).filter_by(jti=jti).scalar()
    return token_exists is not None

if __name__ == "__main__":
    app.run(debug=True)
