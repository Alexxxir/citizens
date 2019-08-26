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

    def to_dict(self) -> dict:
        return {
            "citizen_id": self.citizen_id,
            "town": self.town,
            "street": self.street,
            "building": self.building,
            "apartment": self.apartment,
            "name": self.name,
            "birth_date": self.birth_date.strftime("%d.%m.%Y"),
            "gender": self.gender,
            "relatives": list(
                map(lambda relative: relative.citizen_id, self.relatives)
            ),
        }

    @staticmethod
    def from_dict(dict_citizen: dict) -> "Citizen":
        if not isinstance(dict_citizen, dict):
            raise ValueError(ErrorFieldsMessages.INCORRECT_FIELDS)
        if dict_citizen.keys() != Citizen.SERIALIZED_FIELDS:
            raise ValueError(ErrorFieldsMessages.INCORRECT_FIELDS)
        return Citizen(**dict_citizen)

    def update_from_dict(self, dict_citizen: dict) -> None:
        if Citizen.SERIALIZED_FIELDS > dict_citizen.keys():
            for key, value in dict_citizen.items():
                if key != "relatives":
                    setattr(self, key, value)
            if "relatives" in dict_citizen:
                if not isinstance(dict_citizen["relatives"], list):
                    raise ValueError(ErrorFieldsMessages.INCORRECT_FIELDS)
                existing_ids = {relative.citizen_id for relative in self.relatives}
                new_ids = set(dict_citizen["relatives"])
                remove_relatives_ids = existing_ids - new_ids
                if remove_relatives_ids:
                    remove_relatives = db.session\
                        .query(Citizen)\
                        .filter(Citizen.import_id == self.import_id, Citizen.citizen_id.in_(remove_relatives_ids))\
                        .all()
                    for remove_relative in remove_relatives:
                        if remove_relative in self.relatives:
                            self.relatives.remove(remove_relative)
                        if self in remove_relative.relatives:
                            remove_relative.relatives.remove(self)

                new_relatives_ids = new_ids - existing_ids
                if new_relatives_ids:
                    new_relatives = db.session\
                        .query(Citizen)\
                        .filter(Citizen.import_id == self.import_id, Citizen.citizen_id.in_(new_relatives_ids))\
                        .all()
                    if len(new_relatives) != len(new_relatives_ids):
                        raise ValueError(ErrorFieldsMessages.INCORRECT_FIELDS)
                    for new_relative in new_relatives:
                        if new_relative not in self.relatives:
                            self.relatives.append(new_relative)
                        if self not in new_relative.relatives:
                            new_relative.relatives.append(self)
        else:
            raise ValueError(ErrorFieldsMessages.INCORRECT_FIELDS)
