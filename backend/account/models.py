from backend.database import db, Column, Model, SurrogatePK

class Account(Model):
    __tablename__ = 'account'

    address = Column(db.String(255), primary_key=True)
    balance = Column(db.Integer)