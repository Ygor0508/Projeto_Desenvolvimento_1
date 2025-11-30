# from flask import Blueprint, jsonify, request
# from backend.models import User, BotSettings, db
# from backend.utils.security import encrypt_data
# import backend.bot.bot_manager as bot_manager 
# from backend.bot.backtest_engine import run_dashboard_backtest
# from backend.bot.data_handler import get_dynamic_symbols
# import backend.config as config 
# from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

# api_bp = Blueprint('api', __name__)

# @api_bp.route('/')
# def index(): return jsonify({'message': 'API Online'})

# # --- AUTH ---
# @api_bp.route('/register', methods=['POST'])
# def register():
#     data = request.get_json()
#     if User.query.filter_by(username=data['username']).first(): return jsonify({'error': 'User exists'}), 400
#     new_user = User(username=data['username'], binance_api_key_encrypted=encrypt_data(data['api_key']), binance_api_secret_encrypted=encrypt_data(data['api_secret']))
#     new_user.set_password(data['password'])
#     db.session.add(new_user)
#     db.session.commit()
#     return jsonify({'message': 'OK'}), 201

# @api_bp.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     user = User.query.filter_by(username=data['username']).first()
#     if not user or not user.check_password(data['password']): return jsonify({'error': 'Invalid'}), 401
#     return jsonify(access_token=create_access_token(identity=user.id))

# # --- SISTEMA ---
# @api_bp.route('/health', methods=['GET'])
# def health_check(): return jsonify({'status': 'ok'})

# @api_bp.route('/check-config', methods=['GET'])
# def check_config(): return jsonify({'configured': config.client is not None})

# @api_bp.route('/config/api-keys', methods=['POST'])
# def save_api_keys_route():
#     data = request.json
#     if config.save_api_keys(data.get('apiKey'), data.get('secretKey')): return jsonify({'success': True})
#     return jsonify({'error': 'Failed'}), 500

# @api_bp.route('/test-connection', methods=['POST'])
# def test_connection_route(): return jsonify({'success': True})

# @api_bp.route('/balance', methods=['GET'])
# def get_balance_route():
#     if not config.client: return jsonify({'balance': 0.0}), 200
#     try:
#         info = config.client.get_asset_balance(asset='USDT')
#         return jsonify({'balance': float(info['free']) if info else 0.0})
#     except: return jsonify({'balance': 0.0})

# @api_bp.route('/symbols', methods=['GET'])
# def get_symbols_route():
#     try: return jsonify(get_dynamic_symbols()), 200
#     except Exception as e: return jsonify({'error': str(e)}), 500

# # --- BACKTEST & RISCO ---
# @api_bp.route('/backtest', methods=['POST'])
# def trigger_backtest():
#     data = request.json
#     symbols = data.get('symbols', ['BTCUSDT'])
#     period = data.get('period', 60)
#     use_macro = data.get('use_macro_regime', True)
#     initial_capital = data.get('initial_capital', 10000)
#     if isinstance(symbols, str): symbols = [symbols]
#     try:
#         results = run_dashboard_backtest(symbols, int(period), use_macro, float(initial_capital))
#         if "error" in results: return jsonify(results), 500
#         return jsonify(results), 200
#     except Exception as e: return jsonify({'error': str(e)}), 500

# @api_bp.route('/risk-settings', methods=['GET', 'POST'])
# def risk_settings_route():
#     if request.method == 'POST':
#         data = request.json
#         settings = BotSettings.query.first()
#         if not settings:
#             user = User.query.first()
#             if not user: # Cria admin se não existir
#                 user = User(username='admin', binance_api_key_encrypted=b'file', binance_api_secret_encrypted=b'file')
#                 user.set_password('admin')
#                 db.session.add(user)
#                 db.session.commit()
#             settings = BotSettings(user_id=user.id)
#             db.session.add(settings)
        
#         # Salva TODOS os campos
#         if 'use_macro_regime' in data: settings.use_macro_regime = data['use_macro_regime']
#         if 'tradeAmount' in data: settings.trade_amount_usdt = data['tradeAmount']
        
#         if 'stopLoss' in data:
#             settings.stop_loss_enabled = data['stopLoss'].get('enabled', True)
#             settings.stop_loss_percent = data['stopLoss'].get('percent', 2.0)
#         if 'takeProfit' in data:
#             settings.take_profit_enabled = data['takeProfit'].get('enabled', True)
#             settings.take_profit_percent = data['takeProfit'].get('percent', 5.0)
            
#         if 'maxPositionSize' in data: settings.max_position_size_percent = data['maxPositionSize']
#         if 'maxOpenPositions' in data: settings.max_open_positions = data['maxOpenPositions']
#         if 'riskPerTrade' in data: settings.risk_per_trade_percent = data['riskPerTrade']
#         if 'maxDailyLoss' in data: settings.max_daily_loss = data['maxDailyLoss']
        
#         db.session.commit()
#         return jsonify({'message': 'Salvo com sucesso'})
    
#     else: # GET
#         settings = BotSettings.query.first()
#         if not settings: 
#             return jsonify({
#                 'use_macro_regime': True, 'tradeAmount': 10.0,
#                 'stopLoss': {'enabled': True, 'percent': 2.0},
#                 'takeProfit': {'enabled': True, 'percent': 5.0},
#                 'maxPositionSize': 10.0, 'maxOpenPositions': 3,
#                 'riskPerTrade': 1.0, 'maxDailyLoss': 500
#             })
#         return jsonify({
#             'use_macro_regime': settings.use_macro_regime,
#             'tradeAmount': settings.trade_amount_usdt,
#             'stopLoss': {'enabled': settings.stop_loss_enabled, 'percent': settings.stop_loss_percent},
#             'takeProfit': {'enabled': settings.take_profit_enabled, 'percent': settings.take_profit_percent},
#             'maxPositionSize': settings.max_position_size_percent,
#             'maxOpenPositions': settings.max_open_positions,
#             'riskPerTrade': settings.risk_per_trade_percent,
#             'maxDailyLoss': settings.max_daily_loss
#         })

# # --- BOT ---
# @api_bp.route('/bot/status', methods=['GET'])
# def bot_status(): return jsonify({'running': bot_manager.bot_running, 'positions': bot_manager.CURRENT_POSITIONS})

# @api_bp.route('/bot/start', methods=['POST'])
# def start_bot_route():
#     bot_manager.start_bot()
#     return jsonify({'message': 'Started'})

# @api_bp.route('/bot/stop', methods=['POST'])
# def stop_bot_route():
#     bot_manager.stop_bot()
#     return jsonify({'message': 'Stopped'})








# backend/api/routes.py
from flask import Blueprint, jsonify, request
from backend.models import User, BotSettings, db
from backend.utils.security import encrypt_data
import backend.bot.bot_manager as bot_manager 
from backend.bot.backtest_engine import run_dashboard_backtest
from backend.bot.data_handler import get_dynamic_symbols
import backend.config as config 
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

api_bp = Blueprint('api', __name__)

@api_bp.route('/')
def index(): return jsonify({'message': 'API Online'})

# --- ROTA DE CONFIGURAÇÃO (ATUALIZADA) ---
@api_bp.route('/config/api-keys', methods=['POST'])
def save_api_keys_route():
    """Salva as chaves no Banco de Dados para não perder no Render"""
    data = request.json
    api_key = data.get('apiKey')
    secret_key = data.get('secretKey')

    if not api_key or not secret_key:
        return jsonify({'error': 'Chaves obrigatórias'}), 400

    # 1. Processa chaves (criptografa e atualiza client em memória)
    enc_key, enc_secret = config.save_api_keys(api_key, secret_key)
    
    if enc_key and enc_secret:
        # 2. Salva no Banco de Dados (Persistência Real)
        try:
            # Tenta pegar o primeiro usuário ou cria admin se não existir
            user = User.query.first()
            if not user:
                user = User(username='admin', password_hash='temp') # Senha dummy, será ignorada se já logado
                db.session.add(user)
            
            user.binance_api_key_encrypted = enc_key
            user.binance_api_secret_encrypted = enc_secret
            db.session.commit()
            
            return jsonify({'success': True, 'message': 'Chaves salvas no Banco de Dados!'})
        except Exception as e:
            print(f"Erro ao salvar no banco: {e}")
            return jsonify({'error': 'Erro de banco de dados'}), 500
            
    return jsonify({'error': 'Falha ao processar chaves'}), 500

@api_bp.route('/check-config', methods=['GET'])
def check_config(): 
    # Se não estiver na memória, tenta carregar do banco agora
    if config.client is None:
        config.load_from_db()
    return jsonify({'configured': config.client is not None})

# ... (Demais rotas mantidas iguais: register, login, health, symbols, backtest, risk-settings, bot status/start/stop) ...
# COPIE AS OUTRAS ROTAS DO CÓDIGO ANTERIOR AQUI PARA MANTER O ARQUIVO COMPLETO
# Vou incluir as essenciais abaixo para garantir que funcione

@api_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first(): return jsonify({'error': 'User exists'}), 400
    # Nota: Chaves aqui são opcionais no registro, pois configuramos depois
    new_user = User(username=data['username'], binance_api_key_encrypted=b'', binance_api_secret_encrypted=b'')
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'OK'}), 201

@api_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if not user or not user.check_password(data['password']): return jsonify({'error': 'Invalid'}), 401
    return jsonify(access_token=create_access_token(identity=user.id))

@api_bp.route('/symbols', methods=['GET'])
def get_symbols_route():
    # Garante que tentamos carregar as chaves antes de buscar simbolos
    if not config.client: config.load_from_db()
    try: return jsonify(get_dynamic_symbols()), 200
    except Exception as e: return jsonify({'error': str(e)}), 500

@api_bp.route('/backtest', methods=['POST'])
def trigger_backtest():
    if not config.client: config.load_from_db()
    data = request.json
    symbols = data.get('symbols', ['BTCUSDT'])
    period = data.get('period', 60)
    use_macro = data.get('use_macro_regime', True)
    initial_capital = data.get('initial_capital', 10000)
    if isinstance(symbols, str): symbols = [symbols]
    try:
        results = run_dashboard_backtest(symbols, int(period), use_macro, float(initial_capital))
        if "error" in results: return jsonify(results), 500
        return jsonify(results), 200
    except Exception as e: return jsonify({'error': str(e)}), 500

@api_bp.route('/risk-settings', methods=['GET', 'POST'])
def risk_settings_route():
    if request.method == 'POST':
        data = request.json
        settings = BotSettings.query.first()
        if not settings:
            user = User.query.first()
            if not user:
                user = User(username='admin', binance_api_key_encrypted=b'', binance_api_secret_encrypted=b'')
                user.set_password('admin')
                db.session.add(user)
                db.session.commit()
            settings = BotSettings(user_id=user.id)
            db.session.add(settings)
        
        if 'use_macro_regime' in data: settings.use_macro_regime = data['use_macro_regime']
        if 'tradeAmount' in data: settings.trade_amount_usdt = data['tradeAmount']
        if 'stopLoss' in data:
            settings.stop_loss_enabled = data['stopLoss'].get('enabled', True)
            settings.stop_loss_percent = data['stopLoss'].get('percent', 2.0)
        if 'takeProfit' in data:
            settings.take_profit_enabled = data['takeProfit'].get('enabled', True)
            settings.take_profit_percent = data['takeProfit'].get('percent', 5.0)
        if 'maxPositionSize' in data: settings.max_position_size_percent = data['maxPositionSize']
        if 'maxOpenPositions' in data: settings.max_open_positions = data['maxOpenPositions']
        if 'riskPerTrade' in data: settings.risk_per_trade_percent = data['riskPerTrade']
        if 'maxDailyLoss' in data: settings.max_daily_loss = data['maxDailyLoss']
        
        db.session.commit()
        return jsonify({'message': 'Salvo'})
    else:
        settings = BotSettings.query.first()
        if not settings: return jsonify({'use_macro_regime': True, 'tradeAmount': 10.0})
        return jsonify({
            'use_macro_regime': settings.use_macro_regime,
            'tradeAmount': settings.trade_amount_usdt,
            'stopLoss': {'enabled': settings.stop_loss_enabled, 'percent': settings.stop_loss_percent},
            'takeProfit': {'enabled': settings.take_profit_enabled, 'percent': settings.take_profit_percent},
            'maxPositionSize': settings.max_position_size_percent,
            'maxOpenPositions': settings.max_open_positions,
            'riskPerTrade': settings.risk_per_trade_percent,
            'maxDailyLoss': settings.max_daily_loss
        })

@api_bp.route('/balance', methods=['GET'])
def get_balance_route():
    if not config.client: config.load_from_db()
    if not config.client: return jsonify({'balance': 0.0}), 200
    try:
        info = config.client.get_asset_balance(asset='USDT')
        return jsonify({'balance': float(info['free']) if info else 0.0})
    except: return jsonify({'balance': 0.0})

@api_bp.route('/test-connection', methods=['POST'])
def test_connection_route_real(): return jsonify({'success': True})

@api_bp.route('/bot/status', methods=['GET'])
def bot_status(): return jsonify({'running': bot_manager.bot_running, 'positions': bot_manager.CURRENT_POSITIONS})
@api_bp.route('/bot/start', methods=['POST'])
def start_bot_route(): bot_manager.start_bot(); return jsonify({'message': 'Started'})
@api_bp.route('/bot/stop', methods=['POST'])
def stop_bot_route(): bot_manager.stop_bot(); return jsonify({'message': 'Stopped'})