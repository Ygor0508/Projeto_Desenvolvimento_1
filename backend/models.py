from .database import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import BYTEA

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    binance_api_key_encrypted = db.Column(BYTEA, nullable=False)
    binance_api_secret_encrypted = db.Column(BYTEA, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Trade(db.Model):
    __tablename__ = 'trades'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    symbol = db.Column(db.String(20), nullable=False)
    order_id = db.Column(db.String(50), nullable=False)
    side = db.Column(db.String(4), nullable=False)
    quantity = db.Column(db.Numeric(20, 8), nullable=False)
    price = db.Column(db.Numeric(20, 8), nullable=False)
    total_value_usdt = db.Column(db.Numeric(20, 8), nullable=False)
    pnl_usdt = db.Column(db.Numeric(20, 8))
    timestamp = db.Column(db.DateTime, nullable=False)

class OpenPosition(db.Model):
    __tablename__ = 'open_positions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    symbol = db.Column(db.String(20), unique=True, nullable=False)
    entry_price = db.Column(db.Numeric(20, 8), nullable=False)
    quantity = db.Column(db.Numeric(20, 8), nullable=False)
    entry_timestamp = db.Column(db.DateTime, nullable=False)

class BotSettings(db.Model):
    __tablename__ = 'bot_settings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    is_running = db.Column(db.Boolean, default=False)
    
    # -- Estratégia e Operacional --
    use_macro_regime = db.Column(db.Boolean, default=True)
    trade_amount_usdt = db.Column(db.Float, default=10.0) # Valor fixo por compra
    whitelisted_symbols = db.Column(db.ARRAY(db.Text))
    
    # -- Configurações de Risco --
    stop_loss_enabled = db.Column(db.Boolean, default=True)
    stop_loss_percent = db.Column(db.Float, default=2.0)
    
    take_profit_enabled = db.Column(db.Boolean, default=True)
    take_profit_percent = db.Column(db.Float, default=5.0)
    
    max_position_size_percent = db.Column(db.Float, default=10.0) # Mantido para referência
    max_open_positions = db.Column(db.Integer, default=3)
    risk_per_trade_percent = db.Column(db.Float, default=1.0)
    max_daily_loss = db.Column(db.Float, default=500.0)

    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())