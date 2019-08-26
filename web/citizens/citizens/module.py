import ujson
from flask import Response
from flask.blueprints import Blueprint
from werkzeug.exceptions import HTTPException

from ..utils.api_view import HEADERS
from .views import AddImportView, ImportCitizenView, ImportCitizensListView, ImportBirthdaysView, ImportTownsStateView

module = Blueprint("citizens", __name__)


@module.app_errorhandler(HTTPException)
def http_err_handler(error) -> Response:
    error_message = {"error": {"message": error.description}}
    return Response(ujson.dumps(error_message), error.code, HEADERS)


module.add_url_rule(
    "/imports",
    view_func=AddImportView.as_view("add_import"),
)
module.add_url_rule(
    "/imports/<int:import_id>/citizens/<int:citizen_id>",
    view_func=ImportCitizenView.as_view("citizen"),
)
module.add_url_rule(
    "/imports/<int:import_id>/citizens",
    view_func=ImportCitizensListView.as_view("citizens_list"),
)
module.add_url_rule(
    "/imports/<int:import_id>/citizens/birthdays",
    view_func=ImportBirthdaysView.as_view("birthdays"),
)
module.add_url_rule(
    "/imports/<int:import_id>/towns/stat/percentile/age",
    view_func=ImportTownsStateView.as_view("towns_states"),
)
