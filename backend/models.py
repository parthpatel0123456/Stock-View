from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    # email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    watchlists = db.relationship('Watchlist', backref='user', lazy=True)

    # def set_password(self, password):
    #     self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
class WatchList(db.Model):
    __tablename__ = 'watchlist'
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

User.watchlists = db.relationship('WatchList', backref='user', lazy=True)

class StockNews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), index=True)
    source = db.Column(db.String(120))
    headline = db.Column(db.String(500))
    summary = db.Column(db.String)
    url = db.Column(db.String(500), unique=True, index=True)
    image = db.Column(db.String)
    published_at = db.Column(db.DateTime)
    api = db.Column(db.String)


class StockEarnings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), index=True)
    fiscal_date = db.Column(db.String)
    actual_eps = db.Column(db.Float)
    estimate_eps = db.Column(db.Float)
    surprise = db.Column(db.Float)

class StockFinancials(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), index=True)
    year = db.Column(db.String(10))
    quarter = db.Column(db.String(10))
    assets = db.Column(db.Float)
    liabilites = db.Column(db.Float)
    equity = db.Column(db.Float)
    revenue = db.Column(db.Float)
    net_income = db.Column(db.Float)
    gross_profit = db.Column(db.Float)
    operating_income = db.Column(db.Float)
    operating_cash_flow = db.Column(db.Float)
    investing_cash_flow = db.Column(db.Float)
    financing_cash_flow = db.Column(db.Float)

class StockDividends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(10), index=True)
    cash_amount = db.Column(db.Float)
    ex_dividend_date = db.Column(db.String(20))
    declaration_date = db.Column(db.String(20))
    pay_date = db.Column(db.String(20))
    frequency = db.Column(db.String(20))

    