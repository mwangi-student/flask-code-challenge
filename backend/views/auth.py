from flask import jsonify, request, Blueprint
from models import db, Users, TokenBlocklist
from flask_mail import Message
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt

auth_bp= Blueprint("auth_bp", __name__)


# Login
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data["email"]
    password = data["password"]
    
    user = Users.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password ) :
        access_token = create_access_token(identity=str(user.id))
        return jsonify({"access_token": access_token}), 200

    else:
        return jsonify({"error": "Either email/password is incorrect"}), 404
    

@auth_bp.route("/register", methods=["POST"])
def register():
    from app import mail

    
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    username = data.get("username") 

    if Users.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 409


    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

    new_user = Users(
        email=email,
        password=hashed_password,
        username=username
    )

    db.session.add(new_user)
    db.session.commit()

    # Send welcome email
    msg = Message("Welcome to AfriHouse Realtors",
                  recipients=[email])
    msg.body = f"Hello {username},\n\nThank you for registering with us! We're excited to have you on board.\n\nBest regards,\nAfriHouse Customer Service"
    
    try:
        mail.send(msg)
    except Exception as e:
        print(f"Error sending email: {e}")
        return jsonify({"error": "Failed to send welcome email"}), 500



    return jsonify({"message": "User registered successfully"}), 201

# current user
@auth_bp.route("/current_user", methods=["GET"])
@jwt_required()
def current_user():
    current_user_id  = get_jwt_identity()

    user =  Users.query.get(current_user_id)
    user_data = {
            'id':user.id,
            'email':user.email,
            'username':user.username
        }

    return jsonify(user_data)



# Logout
@auth_bp.route("/logout", methods=["DELETE"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    now = datetime.now(timezone.utc)
    db.session.add(TokenBlocklist(jti=jti, created_at=now))
    db.session.commit()
    return jsonify({"success ":"Logged out successfully"})