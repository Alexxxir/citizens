from typing import Callable, Optional, Dict
from flask.views import MethodView
from flask import Response, request
import ujson


HEADERS: Dict = {
    "Cache-Control": "no-store, no-cache, must-revalidate",
    "Pragma": "no-cache",
    "Content-Type": "application/json; charset=UTF-8",
    "Accept": "application/json, */*; q=0.01",
}


class JsonApiView(MethodView):
    def __init__(self):
        self._data: bytes = request.data
        self._response: Optional[Response] = None

    def dispatch_request(self, *args, **kwargs) -> Response:
        method: Callable = getattr(self, request.method.lower())
        self._response = method(*args, **kwargs)
        self._response.headers = HEADERS
        return self._response

    @property
    def json(self) -> Dict:
        json_data = ujson.loads(self._data)
        if not isinstance(json_data, dict):
            raise ValueError
        return json_data
