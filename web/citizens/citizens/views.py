from flask import Response
from ..utils.api_view import JsonApiView


class AddImportView(JsonApiView):
    def post(self) -> Response:
        pass


class ImportCitizenView(JsonApiView):
    def patch(self, import_id, citizen_id) -> Response:
        pass


class ImportCitizensListView(JsonApiView):
    def get(self, import_id) -> Response:
        pass


class ImportBirthdaysView(JsonApiView):
    def get(self, import_id) -> Response:
        pass


class ImportTownsStateView(JsonApiView):
    def get(self, import_id) -> Response:
        pass
