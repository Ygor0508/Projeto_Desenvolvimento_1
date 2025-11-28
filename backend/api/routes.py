# # backend/api/routes.py
# from flask import Blueprint, jsonify, request
# from backend.models import User, db
# from backend.utils.security import encrypt_data
# from backend.bot.bot_manager import bot_manager
# from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

# api_bp = Blueprint('api', __name__)

# @api_bp.route('/')
# def index():
#     return jsonify({'message': 'API do Trading Bot está no ar!'})

# @api_bp.route('/register', methods=['POST'])
# def register():
#     data = request.get_json()
#     if not all(key in data for key in ['username', 'password', 'api_key', 'api_secret']):
#         return jsonify({'error': 'Dados incompletos'}), 400

#     if User.query.filter_by(username=data['username']).first():
#         return jsonify({'error': 'Usuário já existe'}), 400

#     try:
#         encrypted_api_key = encrypt_data(data['api_key'])
#         encrypted_api_secret = encrypt_data(data['api_secret'])
#     except Exception as e:
#         return jsonify({'error': f'Erro ao criptografar chaves: {e}'}), 500

#     new_user = User(
#         username=data['username'],
#         binance_api_key_encrypted=encrypted_api_key,
#         binance_api_secret_encrypted=encrypted_api_secret
#     )
#     new_user.set_password(data['password'])

#     db.session.add(new_user)
#     db.session.commit()

#     return jsonify({'message': 'Usuário registrado com sucesso!'}), 201

# @api_bp.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     if not data or not data.get('username') or not data.get('password'):
#         return jsonify({'error': 'Dados incompletos'}), 400

#     user = User.query.filter_by(username=data['username']).first()

#     if not user or not user.check_password(data['password']):
#         return jsonify({'error': 'Credenciais inválidas'}), 401

#     access_token = create_access_token(identity=user.id)
#     return jsonify(access_token=access_token)

# @api_bp.route('/bot/start', methods=['POST'])
# @jwt_required()
# def start_bot():
#     current_user_id = get_jwt_identity()
#     success, message = bot_manager.start_bot(current_user_id)
#     if not success:
#         return jsonify({'error': message}), 400
    
#     return jsonify({'message': message}), 200

# @api_bp.route('/bot/stop', methods=['POST'])
# @jwt_required()
# def stop_bot():
#     success, message = bot_manager.stop_bot()
#     if not success:
#         return jsonify({'error': message}), 400

#     return jsonify({'message': message}), 200

# @api_bp.route('/bot/status', methods=['GET'])
# @jwt_required()
# def bot_status():
#     current_user_id = get_jwt_identity()
#     status = bot_manager.get_status(current_user_id)
#     return jsonify(status), 200




# # backend/api/routes.py
# from flask import Blueprint, jsonify, request
# from backend.models import User, db
# from backend.utils.security import encrypt_data
# import backend.bot.bot_manager as bot_manager 
# from backend.bot.backtest_engine import run_dashboard_backtest
# from backend.bot.data_handler import get_dynamic_symbols
# from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

# api_bp = Blueprint('api', __name__)

# # --- ROTAS DE AUTENTICAÇÃO ---

# @api_bp.route('/')
# def index():
#     return jsonify({'message': 'API do Trading Bot está no ar!'})

# @api_bp.route('/register', methods=['POST'])
# def register():
#     data = request.get_json()
#     if not all(key in data for key in ['username', 'password', 'api_key', 'api_secret']):
#         return jsonify({'error': 'Dados incompletos'}), 400

#     if User.query.filter_by(username=data['username']).first():
#         return jsonify({'error': 'Usuário já existe'}), 400

#     try:
#         encrypted_api_key = encrypt_data(data['api_key'])
#         encrypted_api_secret = encrypt_data(data['api_secret'])
#     except Exception as e:
#         return jsonify({'error': f'Erro ao criptografar chaves: {e}'}), 500

#     new_user = User(
#         username=data['username'],
#         binance_api_key_encrypted=encrypted_api_key,
#         binance_api_secret_encrypted=encrypted_api_secret
#     )
#     new_user.set_password(data['password'])

#     db.session.add(new_user)
#     db.session.commit()

#     return jsonify({'message': 'Usuário registrado com sucesso!'}), 201

# @api_bp.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     if not data or not data.get('username') or not data.get('password'):
#         return jsonify({'error': 'Dados incompletos'}), 400

#     user = User.query.filter_by(username=data['username']).first()

#     if not user or not user.check_password(data['password']):
#         return jsonify({'error': 'Credenciais inválidas'}), 401

#     access_token = create_access_token(identity=user.id)
#     return jsonify(access_token=access_token)

# # --- ROTAS NOVAS DO DASHBOARD E BOT ---

# @api_bp.route('/health', methods=['GET'])
# def health_check():
#     return jsonify({'status': 'ok', 'message': 'Trading Bot Backend is running'})

# @api_bp.route('/backtest', methods=['POST'])
# def trigger_backtest():
#     """Rota chamada pelo Dashboard para rodar backtest"""
#     data = request.json
#     symbol = data.get('symbol', 'BTCUSDT')
#     period = data.get('period', 365)
    
#     try:
#         results = run_dashboard_backtest(symbol, int(period))
#         if "error" in results:
#             return jsonify(results), 500
#         return jsonify(results), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @api_bp.route('/bot/status', methods=['GET'])
# def bot_status():
#     """Retorna se o bot está rodando e posições abertas"""
#     return jsonify({
#         'running': bot_manager.bot_running,
#         'positions': bot_manager.CURRENT_POSITIONS
#     })

# @api_bp.route('/bot/start', methods=['POST'])
# @jwt_required()
# def start_bot_route():
#     try:
#         bot_manager.start_bot() 
#         return jsonify({'message': 'Bot iniciado com sucesso'})
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @api_bp.route('/bot/stop', methods=['POST'])
# @jwt_required()
# def stop_bot_route():
#     bot_manager.stop_bot()
#     return jsonify({'message': 'Bot parado'})









# # backend/api/routes.py
# from flask import Blueprint, jsonify, request
# from backend.models import User, db
# from backend.utils.security import encrypt_data
# # Importa o módulo bot_manager inteiro para evitar erros de importação circular
# import backend.bot.bot_manager as bot_manager 
# from backend.bot.backtest_engine import run_dashboard_backtest
# from backend.bot.data_handler import get_dynamic_symbols # <<< Importante para o filtro de ativos
# from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

# api_bp = Blueprint('api', __name__)

# # --- ROTAS DE AUTENTICAÇÃO E SISTEMA ---

# @api_bp.route('/')
# def index():
#     return jsonify({'message': 'API do Trading Bot está no ar!'})

# @api_bp.route('/register', methods=['POST'])
# def register():
#     data = request.get_json()
#     if not all(key in data for key in ['username', 'password', 'api_key', 'api_secret']):
#         return jsonify({'error': 'Dados incompletos'}), 400

#     if User.query.filter_by(username=data['username']).first():
#         return jsonify({'error': 'Usuário já existe'}), 400

#     try:
#         encrypted_api_key = encrypt_data(data['api_key'])
#         encrypted_api_secret = encrypt_data(data['api_secret'])
#     except Exception as e:
#         return jsonify({'error': f'Erro ao criptografar chaves: {e}'}), 500

#     new_user = User(
#         username=data['username'],
#         binance_api_key_encrypted=encrypted_api_key,
#         binance_api_secret_encrypted=encrypted_api_secret
#     )
#     new_user.set_password(data['password'])

#     db.session.add(new_user)
#     db.session.commit()

#     return jsonify({'message': 'Usuário registrado com sucesso!'}), 201

# @api_bp.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     if not data or not data.get('username') or not data.get('password'):
#         return jsonify({'error': 'Dados incompletos'}), 400

#     user = User.query.filter_by(username=data['username']).first()

#     if not user or not user.check_password(data['password']):
#         return jsonify({'error': 'Credenciais inválidas'}), 401

#     access_token = create_access_token(identity=user.id)
#     return jsonify(access_token=access_token)

# @api_bp.route('/health', methods=['GET'])
# def health_check():
#     return jsonify({'status': 'ok', 'message': 'Trading Bot Backend is running'})

# # --- ROTAS DO ROBÔ E DASHBOARD ---

# @api_bp.route('/symbols', methods=['GET'])
# def get_symbols_route():
#     """Retorna a lista de símbolos filtrados pelo robô (Volume > 50M, fora da Blacklist)"""
#     try:
#         symbols = get_dynamic_symbols()
#         return jsonify(symbols), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @api_bp.route('/backtest', methods=['POST'])
# def trigger_backtest():
#     """Rota chamada pelo Dashboard para rodar backtest"""
#     data = request.json
#     symbol = data.get('symbol', 'BTCUSDT')
#     period = data.get('period', 365)
    
#     try:
#         # Chama o motor de backtest dedicado para o dashboard
#         results = run_dashboard_backtest(symbol, int(period))
#         if "error" in results:
#             return jsonify(results), 500
#         return jsonify(results), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @api_bp.route('/bot/status', methods=['GET'])
# def bot_status():
#     """Retorna se o bot está rodando e posições abertas"""
#     return jsonify({
#         'running': bot_manager.bot_running,
#         'positions': bot_manager.CURRENT_POSITIONS
#     })

# @api_bp.route('/bot/start', methods=['POST'])
# @jwt_required()
# def start_bot_route():
#     try:
#         bot_manager.start_bot() 
#         return jsonify({'message': 'Bot iniciado com sucesso'})
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @api_bp.route('/bot/stop', methods=['POST'])
# @jwt_required()
# def stop_bot_route():
#     bot_manager.stop_bot()
#     return jsonify({'message': 'Bot parado'})






# backend/api/routes.py
from flask import Blueprint, jsonify, request
from backend.models import User, db
from backend.utils.security import encrypt_data
# Importa o módulo bot_manager inteiro para evitar erros de importação circular
import backend.bot.bot_manager as bot_manager 
from backend.bot.backtest_engine import run_dashboard_backtest
from backend.bot.data_handler import get_dynamic_symbols
# Importações novas para salvar configuração
import backend.config as config 
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

api_bp = Blueprint('api', __name__)

# --- ROTAS DE CONFIGURAÇÃO (NOVAS) ---

@api_bp.route('/check-config', methods=['GET'])
def check_config():
    """Verifica se as chaves API já estão configuradas no Backend"""
    is_configured = config.client is not None
    return jsonify({'configured': is_configured})

@api_bp.route('/config/api-keys', methods=['POST'])
def save_api_keys_route():
    """Recebe as chaves do frontend, criptografa e salva"""
    data = request.json
    api_key = data.get('apiKey')
    secret_key = data.get('secretKey')

    if not api_key or not secret_key:
        return jsonify({'error': 'Chaves são obrigatórias'}), 400

    success = config.save_api_keys(api_key, secret_key)
    
    if success:
        return jsonify({'success': True, 'message': 'Chaves configuradas com sucesso'})
    else:
        return jsonify({'error': 'Falha ao salvar chaves'}), 500

@api_bp.route('/test-connection', methods=['POST'])
def test_connection_route():
    """Testa a conexão com a Binance usando as chaves fornecidas"""
    # Nota: Em um cenário real, usaríamos o cliente da Binance para fazer um 'ping'
    # Como as chaves já são salvas e testadas no config.py, podemos apenas confirmar
    # se o cliente foi instanciado com sucesso.
    data = request.json
    # Se o front enviar chaves para teste temporário:
    temp_key = data.get('apiKey')
    temp_secret = data.get('secretKey')
    
    try:
        from binance.client import Client
        temp_client = Client(temp_key, temp_secret)
        temp_client.get_account_status() # Teste real
        return jsonify({'success': True, 'message': 'Conexão bem sucedida!'})
    except Exception as e:
        return jsonify({'error': f'Falha na conexão: {str(e)}'}), 400


# --- ROTAS DE AUTENTICAÇÃO E SISTEMA (EXISTENTES) ---

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

@api_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'message': 'Trading Bot Backend is running'})

# --- ROTAS DO ROBÔ E DASHBOARD ---

@api_bp.route('/symbols', methods=['GET'])
def get_symbols_route():
    try:
        symbols = get_dynamic_symbols()
        return jsonify(symbols), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/backtest', methods=['POST'])
def trigger_backtest():
    data = request.json
    symbol = data.get('symbol', 'BTCUSDT')
    period = data.get('period', 365)
    
    try:
        results = run_dashboard_backtest(symbol, int(period))
        if "error" in results:
            return jsonify(results), 500
        return jsonify(results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/bot/status', methods=['GET'])
def bot_status():
    return jsonify({
        'running': bot_manager.bot_running,
        'positions': bot_manager.CURRENT_POSITIONS
    })

@api_bp.route('/bot/start', methods=['POST'])
@jwt_required()
def start_bot_route():
    try:
        bot_manager.start_bot() 
        return jsonify({'message': 'Bot iniciado com sucesso'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/bot/stop', methods=['POST'])
@jwt_required()
def stop_bot_route():
    bot_manager.stop_bot()
    return jsonify({'message': 'Bot parado'})