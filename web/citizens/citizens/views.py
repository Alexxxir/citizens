from flask import Response
from flask.blueprints import Blueprint
from werkzeug.exceptions import HTTPException

from ..utils.api_view import HEADERS

module = Blueprint('citizens', __name__)


@module.app_errorhandler(HTTPException)
def http_err_handler(error):
    return Response(f'{{"error": {{"message": "{error.description}"}}}}',
                    error.code,
                    HEADERS
                    )
