from flask import Response
from flask.blueprints import Blueprint
from werkzeug.exceptions import HTTPException
from ..utils.api_view import JsonApiView, HEADERS
from .models import Citizen

module = Blueprint('citizens', __name__)


@module.app_errorhandler(HTTPException)
def http_err_handler(error):
    return Response(f'{{"error": {{"message": "{error.description}"}}}}',
                    error.code,
                    HEADERS
                    )


class AddImportView(JsonApiView):
    def post(self) -> Response:
        pass


class ImportCitizensListView(JsonApiView):
    def patch(self, import_id, citizen_id):
        pass


class ImportCitizenView(JsonApiView):
    def get(self, import_id):
        pass


class ImportBirthdaysView(JsonApiView):
    def get(self, import_id):
        pass


class ImportTownsStateView(JsonApiView):
    def get(self, import_id):
        pass


module.add_url_rule('/imports', view_func=AddImportView.as_view('add_import'))
module.add_url_rule('/imports/<import_id>/citizens', view_func=ImportCitizensListView.as_view('citizens_list'))
module.add_url_rule('/imports/<import_id>/citizens/<citizen_id>', view_func=ImportCitizenView.as_view('citizen'))
module.add_url_rule('/imports/<import_id>/citizens/birthdays', view_func=ImportBirthdaysView.as_view('birthdays'))
module.add_url_rule('/imports/<import_id>/towns/stat/percentile/age', view_func=ImportTownsStateView.as_view('towns_states'))
