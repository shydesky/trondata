from backend.database import db, Column, Model, SurrogatePK

class Block(Model):
    __tablename__ = 'block'

    number = Column(db.Integer, primary_key=True)
    witness_address = Column(db.String(255))
    timestamp = Column(db.BigInteger)
    blockid = Column(db.String(255))
    parenthash = Column(db.String(255))
    version = Column(db.Integer)