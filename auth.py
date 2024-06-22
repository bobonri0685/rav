from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required
from flask_jwt_extended import create_access_token
from models import User

auth_bp = Blueprint('auth', __name__)

# ... (rota de login) ...
@auth_bp.route('/logout', methods=['POST'])  
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful'}), 200

# ... (função create_admin_user) ...
def create_admin_user():
    admin_username = 'admin'
    admin_password = 'onri0685'
    if not User.query.filter_by(username=admin_username).first():
        admin_user = User(username=admin_username)
        admin_user.password = admin_password
        db.session.add(admin_user)
        db.session.commit()
