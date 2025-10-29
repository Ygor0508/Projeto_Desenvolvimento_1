# backend/api/routes.py
from flask import Blueprint, jsonify, request
from backend.models import User, db
from backend.utils.security import encrypt_data
from backend.bot.bot_manager import bot_manager
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

api_bp = Blueprint('api', __name__)

@api_bp.route('/')
def index():
    return jsonify({'message': 'API do Trading Bot está no ar!'})

@api_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not all(key in data for key in ['username', 'password', 'api_key', 'api_secret']):
        return jsonify({'error': 'Dados incompletos'}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Usuário já existe'}), 400

    try:
        encrypted_api_key = encrypt_data(data['api_key'])
        encrypted_api_secret = encrypt_data(data['api_secret'])
    except Exception as e:
        return jsonify({'error': f'Erro ao criptografar chaves: {e}'}), 500

    new_user = User(
        username=data['username'],
        binance_api_key_encrypted=encrypted_api_key,
        binance_api_secret_encrypted=encrypted_api_secret
    )
    new_user.set_password(data['password'])

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Usuário registrado com sucesso!'}), 201

@api_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Dados incompletos'}), 400

    user = User.query.filter_by(username=data['username']).first()

    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Credenciais inválidas'}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token)

@api_bp.route('/bot/start', methods=['POST'])
@jwt_required()
def start_bot():
    current_user_id = get_jwt_identity()
    success, message = bot_manager.start_bot(current_user_id)
    if not success:
        return jsonify({'error': message}), 400
    
    return jsonify({'message': message}), 200

@api_bp.route('/bot/stop', methods=['POST'])
@jwt_required()
def stop_bot():
    success, message = bot_manager.stop_bot()
    if not success:
        return jsonify({'error': message}), 400

    return jsonify({'message': message}), 200

@api_bp.route('/bot/status', methods=['GET'])
@jwt_required()
def bot_status():
    current_user_id = get_jwt_identity()
    status = bot_manager.get_status(current_user_id)
    return jsonify(status), 200

