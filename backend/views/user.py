from flask import jsonify, request, Blueprint
from models import db, Users, House
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity


user_bp = Blueprint("user_bp", __name__)


# User
@user_bp.route("/users")
def fetch_users():
    users = Users.query.all()

    user_list = []
    for user in users:
        user_list.append({
            'id': user.id,
            'email': user.email,
            'username': user.username,
            "houses": [
                {
                    "id": house.id,
                    "title": house.title,
                    "description": house.description,
                    "location": house.location,
                    "size": house.size,
                    "rent": house.rent,
                    "house_photo": house.house_photo,
                } for house in user.houses  # Use `houses` here
            ]
        })

    return jsonify(user_list)


@user_bp.route("/users/<int:user_id>")
def fetch_single_user(user_id):
    user = Users.query.get(user_id)  # Fetch user by ID
    if not user:
        return jsonify({"error": "User not found"}), 404

    user_data = {
        'id': user.id,
        'email': user.email,
        'username': user.username,
        "houses": [
            {
                "id": house.id,
                "title": house.title,
                "description": house.description,
                "location": house.location,
                "size": house.size,
                "rent": house.rent,
                "house_photo": house.house_photo,
            } for house in user.houses  
        ]
    }

    return jsonify(user_data)


@user_bp.route("/users", methods=["POST"])
def add_users():
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = generate_password_hash(data['password'])

    check_username = Users.query.filter_by(username=username).first()
    check_email = Users.query.filter_by(email=email).first()

    print("Email ",check_email)
    print("Username",check_username)
    if check_username or check_email:
        return jsonify({"error":"Username/email exists"}),406

    else:
        new_user = Users(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"success":"Added successfully"}), 201


# Update
@user_bp.route("/users/<int:user_id>", methods=["PATCH"])
def update_users(user_id):
    user = Users.query.get(user_id)

    if user:
        data = request.get_json()
        username = data.get('username', user.username)
        email = data.get('email', user.email)
        password = data.get('password', user.password)

        check_username = Users.query.filter_by(username=username and id!=user.id).first()
        check_email = Users.query.filter_by(email=email and id!=user.id).first()

    
        if check_username or check_email:
            return jsonify({"error":"Username/email exists"}),406

        else:
            user.username=username
            user.email=email
            user.password=password
          
            db.session.commit()
            return jsonify({"success":"Updated successfully"}), 201

    else:
        return jsonify({"error":"User doesn't exist!"}),406

# Delete
@user_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_users(user_id):
    user = Users.query.get(user_id)

    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"success":"Deleted successfully"}), 200

    else:
        return jsonify({"error":"User your are trying to delete doesn't exist!"}),406

@user_bp.route("/user/delete_account", methods=["DELETE"])
@jwt_required()
def delete_account():
    current_user_id = get_jwt_identity()
    user = Users.query.get(current_user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    houses = House.query.filter_by(user_id=current_user_id).all()
    for house in houses:
        db.session.delete(house)

    db.session.delete(user)
    db.session.commit()
    return jsonify({"success": "User account and associated houses deleted successfully"}), 200