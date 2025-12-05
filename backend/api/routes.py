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








# # backend/api/routes.py
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

# # --- ROTA DE CONFIGURAÇÃO (ATUALIZADA) ---
# @api_bp.route('/config/api-keys', methods=['POST'])
# def save_api_keys_route():
#     data = request.json
#     api_key = data.get('apiKey')
#     secret_key = data.get('secretKey')

#     if not api_key or not secret_key:
#         return jsonify({'error': 'Chaves são obrigatórias'}), 400

#     # 1. Processa chaves
#     try:
#         enc_key, enc_secret = config.save_api_keys(api_key, secret_key)
#         if not enc_key:
#             return jsonify({'error': 'Falha na criptografia das chaves'}), 500
            
#         # 2. Salva no Banco
#         user = User.query.first()
#         if not user:
#             user = User(username='admin', binance_api_key_encrypted=b'', binance_api_secret_encrypted=b'')
#             user.set_password('admin')
#             db.session.add(user)
        
#         # Garante que estamos salvando bytes (Postgres BYTEA)
#         user.binance_api_key_encrypted = enc_key
#         user.binance_api_secret_encrypted = enc_secret
        
#         db.session.commit()
#         return jsonify({'success': True, 'message': 'Chaves salvas com sucesso!'})
        
#     except Exception as e:
#         print(f"ERRO CRÍTICO AO SALVAR CHAVES: {e}")
#         # Retorna o erro real para o frontend (ajuda a debugar)
#         return jsonify({'error': f'Erro interno: {str(e)}'}), 500

# @api_bp.route('/check-config', methods=['GET'])
# def check_config(): 
#     # Se não estiver na memória, tenta carregar do banco agora
#     if config.client is None:
#         config.load_from_db()
#     return jsonify({'configured': config.client is not None})

# # ... (Demais rotas mantidas iguais: register, login, health, symbols, backtest, risk-settings, bot status/start/stop) ...
# # COPIE AS OUTRAS ROTAS DO CÓDIGO ANTERIOR AQUI PARA MANTER O ARQUIVO COMPLETO
# # Vou incluir as essenciais abaixo para garantir que funcione

# @api_bp.route('/register', methods=['POST'])
# def register():
#     data = request.get_json()
#     if User.query.filter_by(username=data['username']).first(): return jsonify({'error': 'User exists'}), 400
#     # Nota: Chaves aqui são opcionais no registro, pois configuramos depois
#     new_user = User(username=data['username'], binance_api_key_encrypted=b'', binance_api_secret_encrypted=b'')
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

# @api_bp.route('/symbols', methods=['GET'])
# def get_symbols_route():
#     # Garante que tentamos carregar as chaves antes de buscar simbolos
#     if not config.client: config.load_from_db()
#     try: return jsonify(get_dynamic_symbols()), 200
#     except Exception as e: return jsonify({'error': str(e)}), 500

# @api_bp.route('/backtest', methods=['POST'])
# def trigger_backtest():
#     if not config.client: config.load_from_db()
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
#             if not user:
#                 user = User(username='admin', binance_api_key_encrypted=b'', binance_api_secret_encrypted=b'')
#                 user.set_password('admin')
#                 db.session.add(user)
#                 db.session.commit()
#             settings = BotSettings(user_id=user.id)
#             db.session.add(settings)
        
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
#         return jsonify({'message': 'Salvo'})
#     else:
#         settings = BotSettings.query.first()
#         if not settings: return jsonify({'use_macro_regime': True, 'tradeAmount': 10.0})
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

# @api_bp.route('/balance', methods=['GET'])
# def get_balance_route():
#     if not config.client: config.load_from_db()
#     if not config.client: return jsonify({'balance': 0.0}), 200
#     try:
#         info = config.client.get_asset_balance(asset='USDT')
#         return jsonify({'balance': float(info['free']) if info else 0.0})
#     except: return jsonify({'balance': 0.0})

# @api_bp.route('/test-connection', methods=['POST'])
# def test_connection_route_real(): return jsonify({'success': True})

# @api_bp.route('/bot/status', methods=['GET'])
# def bot_status(): return jsonify({'running': bot_manager.bot_running, 'positions': bot_manager.CURRENT_POSITIONS})
# @api_bp.route('/bot/start', methods=['POST'])
# def start_bot_route(): bot_manager.start_bot(); return jsonify({'message': 'Started'})
# @api_bp.route('/bot/stop', methods=['POST'])
# def stop_bot_route(): bot_manager.stop_bot(); return jsonify({'message': 'Stopped'})
# def toggle_trading_route():
#     data = request.json
#     action = data.get('action')
    
#     if action == 'start':
#         bot_manager.start_bot()
#         return jsonify({'status': 'started', 'message': 'Robô iniciado'}), 200
#     elif action == 'stop':
#         bot_manager.stop_bot()
#         return jsonify({'status': 'stopped', 'message': 'Robô parado'}), 200
    
#     return jsonify({'error': 'Ação inválida'}), 400










# # backend/api/routes.py
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

# # --- ROTAS DE CONTROLE DO ROBÔ (Prioritárias) ---

# @api_bp.route('/trading/toggle', methods=['POST'])
# def toggle_trading_route():
#     """Liga ou Desliga o Robô via Botão do Dashboard"""
#     data = request.json
#     action = data.get('action')
    
#     try:
#         if action == 'start':
#             bot_manager.start_bot()
#             return jsonify({'status': 'started', 'message': 'Robô iniciado com sucesso'}), 200
#         elif action == 'stop':
#             bot_manager.stop_bot()
#             return jsonify({'status': 'stopped', 'message': 'Robô parado com sucesso'}), 200
#         else:
#             return jsonify({'error': 'Ação desconhecida. Use start ou stop.'}), 400
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @api_bp.route('/bot/status', methods=['GET'])
# def bot_status(): 
#     return jsonify({
#         'running': bot_manager.bot_running, 
#         'positions': bot_manager.CURRENT_POSITIONS
#     })

# @api_bp.route('/bot/start', methods=['POST'])
# def start_bot_route():
#     bot_manager.start_bot()
#     return jsonify({'message': 'Started'})

# @api_bp.route('/bot/stop', methods=['POST'])
# def stop_bot_route():
#     bot_manager.stop_bot()
#     return jsonify({'message': 'Stopped'})

# # --- ROTAS DE SISTEMA E CONFIGURAÇÃO ---

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

# @api_bp.route('/symbols', methods=['GET'])
# def get_symbols_route():
#     try: return jsonify(get_dynamic_symbols()), 200
#     except Exception as e: return jsonify({'error': str(e)}), 500

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
#             if not user:
#                 user = User(username='admin', binance_api_key_encrypted=b'file', binance_api_secret_encrypted=b'file')
#                 user.set_password('admin')
#                 db.session.add(user)
#                 db.session.commit()
#             settings = BotSettings(user_id=user.id)
#             db.session.add(settings)
        
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
#         return jsonify({'message': 'Configurações salvas com sucesso!'})
    
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

# @api_bp.route('/balance', methods=['GET'])
# def get_balance_route():
#     if not config.client: return jsonify({'balance': 0.0}), 200
#     try:
#         info = config.client.get_asset_balance(asset='USDT')
#         return jsonify({'balance': float(info['free']) if info else 0.0})
#     except: return jsonify({'balance': 0.0})





# # backend/api/routes.py
# from flask import Blueprint, jsonify, request
# from backend.models import User, BotSettings, db
# from backend.utils.security import encrypt_data
# import backend.bot.bot_manager as bot_manager 
# from backend.bot.backtest_engine import run_dashboard_backtest
# from backend.bot.data_handler import get_dynamic_symbols
# import backend.config as config 
# from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
# import time

# api_bp = Blueprint('api', __name__)

# @api_bp.route('/')
# def index(): return jsonify({'message': 'API Online'})

# # ==============================================================================
# # --- ROTAS DE DADOS REAIS DA BINANCE (NOVAS) ---
# # ==============================================================================

# @api_bp.route('/binance/account', methods=['GET'])
# def binance_account_info():
#     """Retorna saldo total e status da conta"""
#     if not config.client: return jsonify({'error': 'API não configurada'}), 400
#     try:
#         info = config.client.get_account()
#         # Calcula saldo total estimado em USDT
#         total_balance = 0.0
#         available_usdt = 0.0
        
#         # Tenta pegar cotações para converter altcoins em USDT
#         try:
#             prices = {t['symbol']: float(t['price']) for t in config.client.get_all_tickers()}
#         except:
#             prices = {}
        
#         for bal in info['balances']:
#             free = float(bal['free'])
#             locked = float(bal['locked'])
#             total = free + locked
            
#             if total > 0:
#                 if bal['asset'] == 'USDT':
#                     total_balance += total
#                     available_usdt += free
#                 else:
#                     symbol = f"{bal['asset']}USDT"
#                     if symbol in prices:
#                         total_balance += total * prices[symbol]

#         return jsonify({
#             'totalWalletBalance': total_balance,
#             'availableBalance': available_usdt,
#             'canTrade': info['canTrade']
#         })
#     except Exception as e:
#         print(f"Erro Binance Account: {e}")
#         return jsonify({'error': str(e)}), 500

# @api_bp.route('/binance/positions', methods=['GET'])
# def binance_real_positions():
#     """Retorna o que você realmente tem na carteira (Saldo > 0)"""
#     if not config.client: return jsonify({'positions': []})
#     try:
#         info = config.client.get_account()
#         tickers = config.client.get_all_tickers()
#         prices = {t['symbol']: float(t['price']) for t in tickers}
        
#         positions = []
#         for bal in info['balances']:
#             qty = float(bal['free']) + float(bal['locked'])
#             # Filtra apenas o que não é USDT e tem quantidade
#             if qty > 0 and bal['asset'] != 'USDT':
#                 symbol = f"{bal['asset']}USDT"
#                 current_price = prices.get(symbol, 0)
                
#                 # Só mostra se valer mais que 1 dólar (evita "poeira" de crypto)
#                 if current_price > 0 and (qty * current_price) > 1: 
#                     # Tenta achar preço médio de entrada (aproximado ou do bot)
#                     bot_pos = bot_manager.get_position(symbol)
#                     entry_price = bot_pos['entry_price'] if bot_pos else current_price
                    
#                     pnl = (current_price - entry_price) * qty
#                     pnl_percent = 0.0
#                     if entry_price > 0:
#                         pnl_percent = ((current_price - entry_price) / entry_price) * 100
                    
#                     positions.append({
#                         'symbol': symbol,
#                         'quantity': qty,
#                         'entryPrice': entry_price,
#                         'currentPrice': current_price,
#                         'pnl': pnl,
#                         'pnlPercent': pnl_percent
#                     })
#         return jsonify({'positions': positions})
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @api_bp.route('/binance/trade-history', methods=['GET'])
# def binance_trade_history():
#     """Busca histórico real de trades dos símbolos observados"""
#     if not config.client: return jsonify({'success': False, 'error': 'No config'})
#     try:
#         # Pega símbolos que o bot conhece ou tem modelo
#         symbols_to_check = list(bot_manager.MODELS_AND_REGIME.keys())
#         # Se lista vazia, usa alguns padrões populares para teste
#         if not symbols_to_check: 
#             symbols_to_check = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'ADAUSDT']
        
#         all_trades = []
#         total_commission = 0
        
#         # Limita a 5 símbolos para não demorar demais na resposta da API
#         for symbol in symbols_to_check[:5]:
#             try:
#                 # Busca últimos 10 trades de cada
#                 trades = config.client.get_my_trades(symbol=symbol, limit=10)
#                 for t in trades:
#                     all_trades.append({
#                         'id': str(t['id']),
#                         'symbol': t['symbol'],
#                         'side': 'BUY' if t['isBuyer'] else 'SELL',
#                         'quantity': float(t['qty']),
#                         'price': float(t['price']),
#                         'quoteQty': float(t['quoteQty']),
#                         'commission': float(t['commission']),
#                         'commissionAsset': t['commissionAsset'],
#                         'time': t['time']
#                     })
#                     if t['commissionAsset'] == 'USDT':
#                         total_commission += float(t['commission'])
#                 time.sleep(0.1) # Pequena pausa para evitar rate limit
#             except: pass
            
#         # Ordena por data (mais recente primeiro)
#         all_trades.sort(key=lambda x: x['time'], reverse=True)
        
#         return jsonify({
#             'success': True,
#             'trades': all_trades,
#             'stats': {
#                 'totalTrades': len(all_trades),
#                 'totalCommission': total_commission
#             }
#         })
#     except Exception as e:
#         print(f"Erro History: {e}")
#         return jsonify({'success': False, 'error': str(e)}), 500

# # ==============================================================================
# # --- ROTAS DE CONTROLE DO ROBÔ ---
# # ==============================================================================

# @api_bp.route('/trading/toggle', methods=['POST'])
# def toggle_trading_route():
#     """Liga ou Desliga o Robô via Botão do Dashboard"""
#     data = request.json
#     action = data.get('action')
    
#     try:
#         if action == 'start':
#             bot_manager.start_bot()
#             return jsonify({'status': 'started', 'message': 'Robô iniciado com sucesso'}), 200
#         elif action == 'stop':
#             bot_manager.stop_bot()
#             return jsonify({'status': 'stopped', 'message': 'Robô parado com sucesso'}), 200
#         else:
#             return jsonify({'error': 'Ação desconhecida. Use start ou stop.'}), 400
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @api_bp.route('/bot/status', methods=['GET'])
# def bot_status(): 
#     return jsonify({
#         'running': bot_manager.bot_running, 
#         'positions': bot_manager.CURRENT_POSITIONS
#     })

# @api_bp.route('/bot/start', methods=['POST'])
# def start_bot_route():
#     bot_manager.start_bot()
#     return jsonify({'message': 'Started'})

# @api_bp.route('/bot/stop', methods=['POST'])
# def stop_bot_route():
#     bot_manager.stop_bot()
#     return jsonify({'message': 'Stopped'})

# # ==============================================================================
# # --- ROTAS DE SISTEMA E CONFIGURAÇÃO ---
# # ==============================================================================

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

# @api_bp.route('/health', methods=['GET'])
# def health_check(): return jsonify({'status': 'ok'})

# @api_bp.route('/check-config', methods=['GET'])
# def check_config(): 
#     if config.client is None:
#         config.load_from_db()
#     return jsonify({'configured': config.client is not None})

# @api_bp.route('/config/api-keys', methods=['POST'])
# def save_api_keys_route():
#     data = request.json
#     apiKey = data.get('apiKey')
#     secretKey = data.get('secretKey')
    
#     # 1. Salva no config (Runtime e Arquivo)
#     if config.save_api_keys(apiKey, secretKey):
#         # 2. Salva no Banco de Dados para persistência no Render
#         try:
#             user = User.query.first()
#             if not user:
#                 user = User(username='admin', binance_api_key_encrypted=b'file', binance_api_secret_encrypted=b'file')
#                 user.set_password('admin')
#                 db.session.add(user)
            
#             # Criptografa novamente usando a chave do config
#             from backend.config import cipher
#             enc_key = cipher.encrypt(apiKey.encode())
#             enc_secret = cipher.encrypt(secretKey.encode())
            
#             user.binance_api_key_encrypted = enc_key
#             user.binance_api_secret_encrypted = enc_secret
#             db.session.commit()
#         except Exception as e:
#             print(f"Aviso: Erro ao salvar no DB (mas salvo no arquivo): {e}")
            
#         return jsonify({'success': True})
    
#     return jsonify({'error': 'Failed'}), 500

# @api_bp.route('/test-connection', methods=['POST'])
# def test_connection_route(): return jsonify({'success': True})

# @api_bp.route('/symbols', methods=['GET'])
# def get_symbols_route():
#     try: return jsonify(get_dynamic_symbols()), 200
#     except Exception as e: return jsonify({'error': str(e)}), 500

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
#             if not user:
#                 user = User(username='admin', binance_api_key_encrypted=b'file', binance_api_secret_encrypted=b'file')
#                 user.set_password('admin')
#                 db.session.add(user)
#                 db.session.commit()
#             settings = BotSettings(user_id=user.id)
#             db.session.add(settings)
        
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
#         return jsonify({'message': 'Configurações salvas com sucesso!'})
    
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

# @api_bp.route('/balance', methods=['GET'])
# def get_balance_route():
#     if not config.client: return jsonify({'balance': 0.0}), 200
#     try:
#         info = config.client.get_asset_balance(asset='USDT')
#         return jsonify({'balance': float(info['free']) if info else 0.0})
#     except: return jsonify({'balance': 0.0})






# ULTIMO FUNCIONANDO MAS AINDA ESTA COM ALGUNS BUGS




# from flask import Blueprint, jsonify, request
# from backend.models import User, BotSettings, db
# from backend.utils.security import encrypt_data
# import backend.bot.bot_manager as bot_manager 
# from backend.bot.backtest_engine import run_dashboard_backtest
# from backend.bot.data_handler import get_dynamic_symbols
# import backend.config as config 
# from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
# import time

# api_bp = Blueprint('api', __name__)

# @api_bp.route('/')
# def index(): return jsonify({'message': 'API Online'})

# # ==============================================================================
# # --- ROTAS DE DADOS REAIS (ESTRUTURA RICA PARA O DASHBOARD) ---
# # ==============================================================================

# @api_bp.route('/binance/account', methods=['GET'])
# def binance_account_info():
#     """Retorna saldo total e status da conta"""
#     if not config.client: return jsonify({'error': 'API não configurada'}), 400
#     try:
#         info = config.client.get_account()
#         total_balance = 0.0
#         available_usdt = 0.0
        
#         try:
#             tickers = config.client.get_all_tickers()
#             prices = {t['symbol']: float(t['price']) for t in tickers}
#         except:
#             prices = {}
        
#         for bal in info['balances']:
#             free = float(bal['free'])
#             locked = float(bal['locked'])
#             total = free + locked
            
#             if total > 0:
#                 if bal['asset'] == 'USDT':
#                     total_balance += total
#                     available_usdt += free
#                 else:
#                     symbol = f"{bal['asset']}USDT"
#                     if symbol in prices:
#                         total_balance += total * prices[symbol]

#         return jsonify({
#             'totalWalletBalance': total_balance,
#             'availableBalance': available_usdt,
#             'canTrade': info['canTrade']
#         })
#     except Exception as e:
#         print(f"Erro Account: {e}")
#         return jsonify({'error': str(e)}), 500

# @api_bp.route('/binance/positions', methods=['GET'])
# def binance_real_positions():
#     """
#     Retorna posições reais e cruza com dados da memória do bot 
#     (Stop Loss, Highest Price) para preencher a tabela detalhada.
#     """
#     if not config.client: return jsonify({'positions': []})
#     try:
#         info = config.client.get_account()
#         tickers = config.client.get_all_tickers()
#         prices = {t['symbol']: float(t['price']) for t in tickers}
        
#         positions = []
#         for bal in info['balances']:
#             qty = float(bal['free']) + float(bal['locked'])
            
#             if qty > 0 and bal['asset'] != 'USDT':
#                 symbol = f"{bal['asset']}USDT"
#                 current_price = prices.get(symbol, 0)
                
#                 # Ignora "poeira" (menos de 1 USD)
#                 if current_price > 0 and (qty * current_price) > 1:
                    
#                     # 1. Busca dados da memória do Robô (se ele estiver gerenciando essa moeda)
#                     bot_pos = bot_manager.get_position(symbol)
                    
#                     if bot_pos:
#                         entry_price = float(bot_pos.get('entry_price', current_price))
#                         highest_price = float(bot_pos.get('highest_price', current_price))
#                         stop_loss = float(bot_pos.get('trailing_stop', 0))
#                         is_managed = True
#                     else:
#                         # Se foi compra manual ou antiga (sem registro no bot)
#                         entry_price = current_price # Assume 0% PnL inicial
#                         highest_price = current_price
#                         stop_loss = 0
#                         is_managed = False
                    
#                     # 2. Cálculos Financeiros
#                     total_usdt = qty * current_price
#                     pnl = (current_price - entry_price) * qty
#                     pnl_percent = 0.0
#                     if entry_price > 0:
#                         pnl_percent = ((current_price - entry_price) / entry_price) * 100
                    
#                     positions.append({
#                         'symbol': symbol,
#                         'quantity': qty,
#                         'entryPrice': entry_price,
#                         'currentPrice': current_price,
#                         'highestPrice': highest_price, # Para mostrar o pico
#                         'stopLoss': stop_loss,         # Para mostrar o risco
#                         'totalValue': total_usdt,      # Para mostrar o valor total
#                         'pnl': pnl,
#                         'pnlPercent': pnl_percent,
#                         'isManaged': is_managed        # Se é "AUTÔNOMO" ou manual
#                     })
#         return jsonify({'positions': positions})
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @api_bp.route('/binance/trade-history', methods=['GET'])
# def binance_trade_history():
#     """Busca histórico detalhado para a tabela completa"""
#     if not config.client: return jsonify({'success': False, 'error': 'No config'})
#     try:
#         # Pega simbolos que o bot conhece
#         symbols_to_check = list(bot_manager.MODELS_AND_REGIME.keys())
#         # Fallback para os principais se a lista estiver vazia
#         if not symbols_to_check: 
#             symbols_to_check = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'ADAUSDT']
        
#         all_trades = []
#         total_commission = 0
        
#         # Limita a 5 símbolos para não estourar tempo de resposta
#         for symbol in symbols_to_check[:5]:
#             try:
#                 trades = config.client.get_my_trades(symbol=symbol, limit=10)
#                 for t in trades:
#                     # Formata dados ricos para o frontend
#                     all_trades.append({
#                         'id': str(t['id']),
#                         'symbol': t['symbol'],
#                         'side': 'BUY' if t['isBuyer'] else 'SELL',
#                         'quantity': float(t['qty']),
#                         'price': float(t['price']),
#                         'quoteQty': float(t['quoteQty']), # Total gasto/recebido em USDT
#                         'commission': float(t['commission']),
#                         'commissionAsset': t['commissionAsset'],
#                         'time': t['time']
#                     })
#                     if t['commissionAsset'] == 'USDT':
#                         total_commission += float(t['commission'])
#                 time.sleep(0.1) # Evita rate limit
#             except: pass
            
#         all_trades.sort(key=lambda x: x['time'], reverse=True)
        
#         return jsonify({
#             'success': True,
#             'trades': all_trades,
#             'stats': {
#                 'totalTrades': len(all_trades),
#                 'totalCommission': total_commission
#             }
#         })
#     except Exception as e:
#         print(f"Erro History: {e}")
#         return jsonify({'success': False, 'error': str(e)}), 500

# # ==============================================================================
# # --- ROTAS DE CONTROLE (MANTIDAS) ---
# # ==============================================================================

# @api_bp.route('/trading/toggle', methods=['POST'])
# def toggle_trading_route():
#     data = request.json
#     action = data.get('action')
#     try:
#         if action == 'start':
#             bot_manager.start_bot()
#             return jsonify({'status': 'started', 'message': 'Robô iniciado'}), 200
#         elif action == 'stop':
#             bot_manager.stop_bot()
#             return jsonify({'status': 'stopped', 'message': 'Robô parado'}), 200
#         else:
#             return jsonify({'error': 'Ação inválida'}), 400
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# @api_bp.route('/bot/status', methods=['GET'])
# def bot_status(): 
#     return jsonify({
#         'running': bot_manager.bot_running, 
#         'positions': bot_manager.CURRENT_POSITIONS
#     })

# @api_bp.route('/bot/start', methods=['POST'])
# def start_bot_route():
#     bot_manager.start_bot()
#     return jsonify({'message': 'Started'})

# @api_bp.route('/bot/stop', methods=['POST'])
# def stop_bot_route():
#     bot_manager.stop_bot()
#     return jsonify({'message': 'Stopped'})

# # ==============================================================================
# # --- ROTAS DE SISTEMA (MANTIDAS) ---
# # ==============================================================================

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

# @api_bp.route('/health', methods=['GET'])
# def health_check(): return jsonify({'status': 'ok'})

# @api_bp.route('/check-config', methods=['GET'])
# def check_config(): 
#     if config.client is None: config.load_from_db()
#     return jsonify({'configured': config.client is not None})

# @api_bp.route('/config/api-keys', methods=['POST'])
# def save_api_keys_route():
#     data = request.json
#     apiKey = data.get('apiKey')
#     secretKey = data.get('secretKey')
#     if config.save_api_keys(apiKey, secretKey):
#         try:
#             user = User.query.first()
#             if not user:
#                 user = User(username='admin', binance_api_key_encrypted=b'file', binance_api_secret_encrypted=b'file')
#                 user.set_password('admin')
#                 db.session.add(user)
#             from backend.config import cipher
#             user.binance_api_key_encrypted = cipher.encrypt(apiKey.encode())
#             user.binance_api_secret_encrypted = cipher.encrypt(secretKey.encode())
#             db.session.commit()
#         except: pass
#         return jsonify({'success': True})
#     return jsonify({'error': 'Failed'}), 500

# @api_bp.route('/test-connection', methods=['POST'])
# def test_connection_route(): return jsonify({'success': True})

# @api_bp.route('/symbols', methods=['GET'])
# def get_symbols_route():
#     try: return jsonify(get_dynamic_symbols()), 200
#     except Exception as e: return jsonify({'error': str(e)}), 500

# @api_bp.route('/backtest', methods=['POST'])
# def trigger_backtest():
#     data = request.json
#     try:
#         results = run_dashboard_backtest(data.get('symbols', ['BTCUSDT']), int(data.get('period', 60)), data.get('use_macro_regime', True), float(data.get('initial_capital', 10000)))
#         return jsonify(results), 200
#     except Exception as e: return jsonify({'error': str(e)}), 500

# @api_bp.route('/risk-settings', methods=['GET', 'POST'])
# def risk_settings_route():
#     if request.method == 'POST':
#         return jsonify({'message': 'Salvo'})
#     else:
#         return jsonify({
#             'use_macro_regime': True, 'tradeAmount': 10.0,
#             'stopLoss': {'enabled': True, 'percent': 2.0},
#             'takeProfit': {'enabled': True, 'percent': 5.0},
#             'maxPositionSize': 10.0, 'maxOpenPositions': 3,
#             'riskPerTrade': 1.0, 'maxDailyLoss': 500
#         })

# @api_bp.route('/balance', methods=['GET'])
# def get_balance_route():
#     if not config.client: return jsonify({'balance': 0.0}), 200
#     try:
#         info = config.client.get_asset_balance(asset='USDT')
#         return jsonify({'balance': float(info['free']) if info else 0.0})
#     except: return jsonify({'balance': 0.0})










from flask import Blueprint, jsonify, request
from backend.models import User, BotSettings, db
from backend.utils.security import encrypt_data
import backend.bot.bot_manager as bot_manager 
from backend.bot.backtest_engine import run_dashboard_backtest
from backend.bot.data_handler import get_dynamic_symbols
import backend.config as config 
from flask_jwt_extended import create_access_token
import time

api_bp = Blueprint('api', __name__)

@api_bp.route('/')
def index(): return jsonify({'message': 'API Online'})

# ==============================================================================
# --- DADOS REAIS (BINANCE) - CORREÇÃO DO HISTÓRICO ---
# ==============================================================================

@api_bp.route('/binance/account', methods=['GET'])
def binance_account_info():
    if not config.client: return jsonify({'error': 'API não configurada'}), 400
    try:
        info = config.client.get_account()
        total_balance = 0.0
        available_usdt = 0.0
        
        try:
            tickers = config.client.get_all_tickers()
            prices = {t['symbol']: float(t['price']) for t in tickers}
        except: prices = {}
        
        for bal in info['balances']:
            free = float(bal['free'])
            locked = float(bal['locked'])
            total = free + locked
            if total > 0:
                if bal['asset'] == 'USDT':
                    total_balance += total
                    available_usdt += free
                else:
                    symbol = f"{bal['asset']}USDT"
                    if symbol in prices:
                        total_balance += total * prices[symbol]

        return jsonify({
            'totalWalletBalance': total_balance,
            'availableBalance': available_usdt,
            'canTrade': info['canTrade']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/binance/positions', methods=['GET'])
def binance_real_positions():
    if not config.client: return jsonify({'positions': []})
    try:
        info = config.client.get_account()
        tickers = config.client.get_all_tickers()
        prices = {t['symbol']: float(t['price']) for t in tickers}
        
        positions = []
        for bal in info['balances']:
            qty = float(bal['free']) + float(bal['locked'])
            if qty > 0 and bal['asset'] != 'USDT':
                symbol = f"{bal['asset']}USDT"
                current_price = prices.get(symbol, 0)
                
                if current_price > 0 and (qty * current_price) > 1:
                    bot_pos = bot_manager.get_position(symbol)
                    entry_price = bot_pos['entry_price'] if bot_pos else current_price
                    pnl = (current_price - entry_price) * qty
                    pnl_percent = ((current_price - entry_price) / entry_price * 100) if entry_price > 0 else 0
                    
                    positions.append({
                        'symbol': symbol,
                        'quantity': qty,
                        'entryPrice': entry_price,
                        'currentPrice': current_price,
                        'pnl': pnl,
                        'pnlPercent': pnl_percent,
                        'totalValue': qty * current_price,
                        'stopLoss': bot_pos.get('trailing_stop', 0) if bot_pos else 0,
                        'highestPrice': bot_pos.get('highest_price', 0) if bot_pos else 0,
                        'isManaged': bot_pos is not None
                    })
        return jsonify({'positions': positions})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/binance/trade-history', methods=['GET'])
def binance_trade_history():
    """Busca histórico das moedas que você REALMENTE tem ou operou"""
    if not config.client: return jsonify({'success': False, 'error': 'API offline'})
    try:
        # 1. Identifica quais símbolos verificar (Ativos na carteira + Padrões)
        symbols_to_check = set(['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT']) # Padrão
        
        # Adiciona o que o bot está operando
        symbols_to_check.update(bot_manager.MODELS_AND_REGIME.keys())
        
        # Adiciona o que você tem na carteira (Lógica Inteligente)
        try:
            info = config.client.get_account()
            for bal in info['balances']:
                if float(bal['free']) + float(bal['locked']) > 0:
                    if bal['asset'] != 'USDT':
                        symbols_to_check.add(f"{bal['asset']}USDT")
        except: pass

        all_trades = []
        total_commission = 0
        
        # Busca histórico (Limite de 8 símbolos para não travar)
        for symbol in list(symbols_to_check)[:8]: 
            try:
                trades = config.client.get_my_trades(symbol=symbol, limit=10)
                for t in trades:
                    all_trades.append({
                        'id': str(t['id']),
                        'symbol': t['symbol'],
                        'side': 'BUY' if t['isBuyer'] else 'SELL',
                        'quantity': float(t['qty']),
                        'price': float(t['price']),
                        'quoteQty': float(t['quoteQty']),
                        'commission': float(t['commission']),
                        'commissionAsset': t['commissionAsset'],
                        'time': t['time']
                    })
                    if t['commissionAsset'] == 'USDT':
                        total_commission += float(t['commission'])
                time.sleep(0.05)
            except: pass # Ignora erro se par não existir (ex: NFTUSDT)
            
        all_trades.sort(key=lambda x: x['time'], reverse=True)
        
        return jsonify({
            'success': True,
            'trades': all_trades,
            'stats': {
                'totalTrades': len(all_trades),
                'totalCommission': total_commission,
                'totalPnL': 0, # Difícil calcular PnL exato histórico sem tracking completo
                'winRate': 0
            }
        })
    except Exception as e:
        print(f"Erro History: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

# ==============================================================================
# --- GESTÃO DE RISCO (CORREÇÃO DO SALVAMENTO) ---
# ==============================================================================

@api_bp.route('/risk-settings', methods=['GET', 'POST'])
def risk_settings_route():
    # Garante que existe usuário Admin
    user = User.query.first()
    if not user:
        try:
            user = User(username='admin', binance_api_key_encrypted=b'', binance_api_secret_encrypted=b'')
            user.set_password('admin')
            db.session.add(user)
            db.session.commit()
        except: db.session.rollback()

    if request.method == 'POST':
        data = request.json
        settings = BotSettings.query.first()
        if not settings:
            settings = BotSettings(user_id=user.id)
            db.session.add(settings)
        
        # Salva dados recebidos
        if 'use_macro_regime' in data: settings.use_macro_regime = data['use_macro_regime']
        if 'tradeAmount' in data: settings.trade_amount_usdt = float(data['tradeAmount'])
        
        if 'stopLoss' in data:
            settings.stop_loss_enabled = data['stopLoss'].get('enabled', True)
            settings.stop_loss_percent = float(data['stopLoss'].get('percent', 2.0))
        
        if 'takeProfit' in data:
            settings.take_profit_enabled = data['takeProfit'].get('enabled', True)
            settings.take_profit_percent = float(data['takeProfit'].get('percent', 5.0))
            
        if 'maxPositionSize' in data: settings.max_position_size_percent = float(data['maxPositionSize'])
        if 'maxOpenPositions' in data: settings.max_open_positions = int(data['maxOpenPositions'])
        if 'riskPerTrade' in data: settings.risk_per_trade_percent = float(data['riskPerTrade'])
        if 'maxDailyLoss' in data: settings.max_daily_loss = float(data['maxDailyLoss'])
        
        try:
            db.session.commit()
            return jsonify({'message': 'Configurações salvas com sucesso!'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    else: # GET
        settings = BotSettings.query.first()
        # Valores Default se não existir no banco
        defaults = {
            'use_macro_regime': True, 'tradeAmount': 10.0,
            'stopLoss': {'enabled': True, 'percent': 2.0},
            'takeProfit': {'enabled': True, 'percent': 5.0},
            'maxPositionSize': 10.0, 'maxOpenPositions': 3,
            'riskPerTrade': 1.0, 'maxDailyLoss': 500
        }
        
        if not settings: return jsonify(defaults)
        
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

# ==============================================================================
# --- ROTAS DE SISTEMA (MANTIDAS) ---
# ==============================================================================

@api_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(username=data['username']).first(): return jsonify({'error': 'User exists'}), 400
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

@api_bp.route('/check-config', methods=['GET'])
def check_config(): 
    if config.client is None: config.load_from_db()
    return jsonify({'configured': config.client is not None})

@api_bp.route('/config/api-keys', methods=['POST'])
def save_api_keys_route():
    data = request.json
    if config.save_api_keys(data.get('apiKey'), data.get('secretKey')):
        # Tenta persistir no banco para garantir
        try:
            user = User.query.first()
            if not user:
                user = User(username='admin', binance_api_key_encrypted=b'', binance_api_secret_encrypted=b'')
                user.set_password('admin')
                db.session.add(user)
            from backend.config import cipher
            user.binance_api_key_encrypted = cipher.encrypt(data.get('apiKey').encode())
            user.binance_api_secret_encrypted = cipher.encrypt(data.get('secretKey').encode())
            db.session.commit()
        except: pass
        return jsonify({'success': True})
    return jsonify({'error': 'Failed'}), 500

@api_bp.route('/test-connection', methods=['POST'])
def test_connection_route(): return jsonify({'success': True})

@api_bp.route('/symbols', methods=['GET'])
def get_symbols_route():
    try: return jsonify(get_dynamic_symbols()), 200
    except Exception as e: return jsonify({'error': str(e)}), 500

@api_bp.route('/backtest', methods=['POST'])
def trigger_backtest():
    data = request.json
    try:
        results = run_dashboard_backtest(data.get('symbols', ['BTCUSDT']), int(data.get('period', 60)), data.get('use_macro_regime', True), float(data.get('initial_capital', 10000)))
        return jsonify(results), 200
    except Exception as e: return jsonify({'error': str(e)}), 500

@api_bp.route('/balance', methods=['GET'])
def get_balance_route():
    if not config.client: return jsonify({'balance': 0.0}), 200
    try:
        info = config.client.get_asset_balance(asset='USDT')
        return jsonify({'balance': float(info['free']) if info else 0.0})
    except: return jsonify({'balance': 0.0})

# Bot Control
@api_bp.route('/bot/status', methods=['GET'])
def bot_status(): return jsonify({'running': bot_manager.bot_running, 'positions': bot_manager.CURRENT_POSITIONS})
@api_bp.route('/bot/start', methods=['POST'])
def start_bot_route(): bot_manager.start_bot(); return jsonify({'message': 'Started'})
@api_bp.route('/bot/stop', methods=['POST'])
def stop_bot_route(): bot_manager.stop_bot(); return jsonify({'message': 'Stopped'})
@api_bp.route('/trading/toggle', methods=['POST'])
def toggle_trading_route():
    data = request.json
    if data.get('action') == 'start': bot_manager.start_bot(); return jsonify({'status': 'started'})
    if data.get('action') == 'stop': bot_manager.stop_bot(); return jsonify({'status': 'stopped'})
    return jsonify({'error': 'Invalid'}), 400