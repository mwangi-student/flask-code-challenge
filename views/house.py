from flask import jsonify, request, Blueprint
from models import db, Users, House
from flask_jwt_extended import jwt_required, get_jwt_identity

house_bp = Blueprint("house_bp", __name__)

# ==================================TO--DO======================================

@house_bp.route("/house/add", methods=["POST"])
@jwt_required()
def add_house():
    data = request.get_json()
    current_user_id = get_jwt_identity()

    title = data['title']
    description = data['description']
    user_id = data['user_id']
    location = data['location']
    size = data['size']
    house_photo = data['house_photo']
    rent = data['rent']

    check_user_id = Users.query.get(user_id)

    if not check_user_id:
        return jsonify({"error":"User doesn't exists"}),406

    else:
        new_house = House(title = title, description = description, user_id = current_user_id, location=location, size = size, house_photo = house_photo, rent = rent)
        db.session.add(new_house)
        db.session.commit()
        return jsonify({"success":"House added successfully"}), 201

@house_bp.route("/house/delete/<int:house_id>", methods=["DELETE"])
@jwt_required()
def delete_house(house_id):
    current_user_id = get_jwt_identity()
    house = House.query.get(house_id)

    if not house:
        return jsonify({"error": "House not found"}), 404

    if house.user_id != current_user_id:
        return jsonify({"error": "Unauthorized to delete this house"}), 403

    db.session.delete(house)
    db.session.commit()
    return jsonify({"success": "House deleted successfully"}), 200

@house_bp.route("/house/update/<int:house_id>", methods=["PUT"])
@jwt_required()
def update_house(house_id):
    data = request.get_json()
    current_user_id = get_jwt_identity()
    house = House.query.get(house_id)

    if not house:
        return jsonify({"error": "House not found"}), 404

    if house.user_id != current_user_id:
        return jsonify({"error": "Unauthorized to update this house"}), 403

    house.title = data.get('title', house.title)
    house.description = data.get('description', house.description)
    house.location = data.get('location', house.location)
    house.size = data.get('size', house.size)
    house.house_photo = data.get('house_photo', house.house_photo)
    house.rent = data.get('rent', house.rent)

    db.session.commit()
    return jsonify({"success": "House updated successfully"}), 200


