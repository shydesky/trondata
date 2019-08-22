from backend.database import db, Column, Model, SurrogatePK

class Witness(Model):
    __tablename__ = 'witness'

    address = Column(db.String(255), primary_key=True)
    name = Column(db.String(255))
    address_b58c = Column(db.String(64))
    
    def __str__(self):
        return '(%s, %s, %s)' % (self.name, self.address_b58c, self.address)

class WitnessSchedule(SurrogatePK, Model):
    __tablename__ = 'witness_schedule'

    timestamp_start = Column(db.Integer)
    timestamp_end = Column(db.Integer)
    witness_list = Column(db.String(4096))
    block_number_start = Column(db.Integer)
    block_number_end = Column(db.Integer)