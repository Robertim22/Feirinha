from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(100), nullable=False)
    valor_compra = db.Column(db.Float, nullable=False)
    valor_venda = db.Column(db.Float, nullable=False)
    lote = db.Column(db.String(100), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
