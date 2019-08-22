from typing import Callable, Optional, Dict
from flask.views import MethodView
from flask import Response, request
from werkzeug.exceptions import BadRequest
try:
    import ujson as json
except ModuleNotFoundError:
    import json


HEADERS: Dict = {
    "Cache-Control": "no-store, no-cache, must-revalidate",
    "Pragma": "no-cache",
    "Content-Type": "application/json; charset=UTF-8",
    "Accept": "application/json, */*; q=0.01"
}


class JsonApiView(MethodView):
    def __init__(self):
        self._data: bytes = request.data
        self._json: Optional[Dict] = None
        self._response: Optional[Response] = None

    def dispatch_request(self, *args, **kwargs) -> Response:
        method: Callable = getattr(self, request.method.lower())
        self._response = method(*args, **kwargs)
        self._response.headers = HEADERS
        return self._response

    @property
    def json(self) -> Dict:
        if not self._json:
            try:
                self._json = json.loads(self._data)
                if not isinstance(self._json, dict):
                    raise ValueError
            except ValueError:
                raise BadRequest("Данные должны быть в формате json")
        return self._json
