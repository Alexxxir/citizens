from ..database import db
from sqlalchemy.dialects.postgresql import ENUM


class RelatedCommunication(db.Model):
    __tablename__ = 'related_communications'
    citizen_id = db.Column(db.Integer(), db.ForeignKey('citizens.id'), primary_key=True)
    relative_id = db.Column(db.Integer(), db.ForeignKey('citizens.id'), primary_key=True)


class Citizen(db.Model):
    __tablename__ = 'citizens'
    __table_args__ = (
        db.Index('index_1', 'import_id', 'citizen_id', unique=True),
    )

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    import_id = db.Column(db.Integer(), nullable=False)
    citizen_id = db.Column(db.Integer(), nullable=False)
    town = db.Column(db.String(256), nullable=False)
    street = db.Column(db.String(256), nullable=False)
    building = db.Column(db.String(256), nullable=False)
    apartment = db.Column(db.Integer(), nullable=False)
    name = db.Column(db.String(256), nullable=False)
    birth_date = db.Column(db.Date(), nullable=False)
    gender = db.Column(ENUM('female', 'male', name='gender'))
    relatives = db.relationship('Citizen', 'related_communications',
                                primaryjoin=RelatedCommunication.citizen_id==id,
                                secondaryjoin=RelatedCommunication.relative_id==id)


