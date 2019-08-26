import datetime
from numpy import percentile
import ujson
from flask import Response
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import BadRequest, NotFound
from ..utils.api_view import JsonApiView
from ..database import db
from .models import Citizen, RelatedCommunication
from http import HTTPStatus
from .error_messages import ErrorMessages


class AddImportView(JsonApiView):
    def post(self) -> Response:
        try:
            request_data = self.json
        except ValueError:
            raise BadRequest(ErrorMessages.NOT_JSON_FORMAT)
        if (not isinstance(request_data.get("citizens", None), list) or
                request_data.keys() != {"citizens"}):
            raise BadRequest(ErrorMessages.INCORRECT_DATA_FORMAT)
        try:
            citizens = {
                citizen["citizen_id"]: Citizen.from_dict(citizen)
                for citizen in request_data["citizens"]
            }
        except ValueError as e:
            raise BadRequest(e)
        if len(citizens) != len(request_data["citizens"]):
            raise BadRequest(ErrorMessages.INCORRECT_DATA_FORMAT)

        citizens_list = list(citizens.values())

        try:
            for citizen in citizens_list:
                citizen.relatives = [citizens[relative] for relative in citizen.relatives]
        except KeyError:
            raise BadRequest(ErrorMessages.INCORRECT_RELATIVES)

        for citizen in citizens_list:
            for relative in citizen.relatives:
                if citizen not in relative.relatives:
                    raise BadRequest(ErrorMessages.INCORRECT_RELATIVES)

        try:
            next_id = db.session.query(db.func.nextval('import_id_seq')).first()[0][0]
            for citizen in citizens_list:
                citizen.import_id = next_id

            db.session.add_all(citizens_list)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

        json_data = {"data": {"import_id": next_id}}
        return Response(ujson.dumps(json_data), HTTPStatus.CREATED)


class ImportCitizenView(JsonApiView):
    def patch(self, import_id, citizen_id) -> Response:
        try:
            json_data = self.json
        except ValueError:
            raise BadRequest(ErrorMessages.NOT_JSON_FORMAT)
        citizen = db.session.query(Citizen) \
            .filter(Citizen.import_id == import_id, Citizen.citizen_id == citizen_id) \
            .limit(1) \
            .first()

        if not citizen:
            raise NotFound(
                ErrorMessages.NOT_FOUND_CITIZEN
            )
        try:
            citizen.update_from_dict(json_data)
        except ValueError as e:
            raise BadRequest(e)

        try:
            db.session.add(citizen)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e

        json_data = {"data": citizen.to_dict()}
        return Response(ujson.dumps(json_data), HTTPStatus.OK)


class ImportCitizensListView(JsonApiView):
    def get(self, import_id) -> Response:
        citizens = db.session.query(Citizen) \
            .options(db.joinedload(Citizen.relatives)) \
            .filter(Citizen.import_id == import_id) \
            .all()
        if not citizens:
            raise NotFound(ErrorMessages.NOT_FOUND_IMPORT)

        results = {
            "data": [citizen.to_dict() for citizen in citizens]
        }
        return Response(ujson.dumps(results), HTTPStatus.OK)


class ImportBirthdaysView(JsonApiView):
    def get(self, import_id) -> Response:
        results = {"data": {str(i + 1): [] for i in range(12)}}
        relatives = db.aliased(Citizen, name='relative')
        subq = db.session\
            .query(
                Citizen.citizen_id,
                RelatedCommunication.relative_id,
                db.extract('month', relatives.birth_date).label("month")) \
            .join(RelatedCommunication, RelatedCommunication.citizen_id == Citizen.id) \
            .join(relatives, relatives.id == RelatedCommunication.relative_id) \
            .filter(Citizen.import_id == import_id) \
            .cte()
        relatives_birth_month_count = db.session\
            .query(subq.c.citizen_id, subq.c.month, db.func.count(subq.c.relative_id))\
            .group_by(subq.c.citizen_id, subq.c.month)\
            .all()
        if not relatives_birth_month_count:
            raise NotFound(ErrorMessages.NOT_FOUND_IMPORT)

        for citizen_id, month, count in relatives_birth_month_count:
            results["data"][str(int(month))].append({"citizen_id": citizen_id, "presents": count})
        return Response(ujson.dumps(results), HTTPStatus.OK)


class ImportTownsStateView(JsonApiView):
    def get(self, import_id) -> Response:
        today = datetime.datetime.utcnow().date()
        birth_dates_in_towns = db.session\
            .query(Citizen.town, Citizen.birth_date)\
            .filter(Citizen.import_id == import_id)\
            .all()

        if not birth_dates_in_towns:
            raise NotFound(ErrorMessages.NOT_FOUND_IMPORT)

        ages_in_towns = {}
        for town, birth_date in birth_dates_in_towns:
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            ages_in_towns.setdefault(town, []).append(age)

        results = {
            "data": [
                {
                    "town": town,
                    "p50": round(percentile(ages, 50), 2),
                    "p75": round(percentile(ages, 75), 2),
                    "p99": round(percentile(ages, 99), 2)
                }
                for town, ages in ages_in_towns.items()
            ]
        }
        return Response(ujson.dumps(results), HTTPStatus.OK)
