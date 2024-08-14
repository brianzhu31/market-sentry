from flask import jsonify, request, Blueprint, g
from config import supabase
from models import db, User
from utils.validation import token_required

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
@token_required
def register_user():
    user = g.user

    user_id = user["sub"]
    email = user["email"]

    new_user = User(
        id=user_id,
        email=email,
    )

    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400

    return {"message": "User created."}, 201
