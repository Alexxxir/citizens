from .error_messages import ErrorMessages, ErrorFieldsMessages
from .validators import validate_address, validate_birth_date
from ..database import db
from sqlalchemy.dialects.postgresql import ENUM


class RelatedCommunication(db.Model):
    __tablename__ = "related_communications"

    citizen_id = db.Column(db.Integer(), db.ForeignKey("citizens.id"), primary_key=True)
    relative_id = db.Column(
        db.Integer(), db.ForeignKey("citizens.id"), primary_key=True
    )


class Citizen(db.Model):
    __tablename__ = "citizens"
    __table_args__ = (
        db.Index("index_1", "import_id", "citizen_id", unique=True),
        db.Index("index_2", "import_id"),
    )
    SERIALIZED_FIELDS = {
        "citizen_id",
        "town",
        "street",
        "building",
        "apartment",
        "name",
        "birth_date",
        "gender",
        "relatives",
    }
    GENDER = ENUM("female", "male", name="gender")

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    import_id = db.Column(db.Integer(), nullable=False)
    citizen_id = db.Column(db.Integer(), nullable=False)
    town = db.Column(db.String(256), nullable=False)
    street = db.Column(db.String(256), nullable=False)
    building = db.Column(db.String(256), nullable=False)
    apartment = db.Column(db.Integer(), nullable=False)
    name = db.Column(db.String(256), nullable=False)
    birth_date = db.Column(db.Date(), nullable=False)
    gender = db.Column(GENDER)
    relatives = db.relationship(
        "Citizen",
        "related_communications",
        primaryjoin=RelatedCommunication.citizen_id == id,
        secondaryjoin=RelatedCommunication.relative_id == id,
    )

    @db.validates("citizen_id")
    def validate_citizen_id(self, key, citizen_id):
        if isinstance(citizen_id, int) and citizen_id >= 0:
            return citizen_id
        raise ValueError(ErrorFieldsMessages.INCORRECT_CITIZEN_ID)

    @db.validates("town")
    def validate_town(self, key, town):
        return validate_address(town, key)

    @db.validates("street")
    def validate_street(self, key, street):
        return validate_address(street, key)

    @db.validates("building")
    def validate_building(self, key, building):
        return validate_address(building, key)

    @db.validates("apartment")
    def validate_apartment(self, key, apartment):
        if isinstance(apartment, int) and apartment >= 0:
            return apartment
        raise ValueError(ErrorFieldsMessages.INCORRECT_APARTMENT)

    @db.validates("name")
    def validate_name(self, key, name):
        if isinstance(name, str) and 0 < len(name) <= 256:
            return name
        raise ValueError(ErrorFieldsMessages.INCORRECT_NAME)

    @db.validates("birth_date")
    def validate_birth_date(self, key, birth_date):
        return validate_birth_date(birth_date)

    @db.validates("gender")
    def validate_gender(self, key, gender):
        if gender in Citizen.GENDER.enums:
            return gender
        raise ValueError(ErrorFieldsMessages.INCORRECT_GENDER)
