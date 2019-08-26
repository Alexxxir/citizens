from http import HTTPStatus

import pytest
from hamcrest import has_property, assert_that, all_of
from .matchers import has_status, has_error_answer


@pytest.mark.parametrize(
    "handler",
    ["/", "/notfound", "/import", "/import", "/imports/test/citizens/birthdays"]
)
def test_nonexistent_handlers(client, handler):
    assert_that(
        client.get(handler),
        all_of(
            has_property("json", has_error_answer()),
            has_status(HTTPStatus.NOT_FOUND)
        )
    )


@pytest.mark.parametrize(
    "handler",
    ["/imports", "/imports/1/citizens/1"]
)
def test_not_allowed_methods(client, handler):
    assert_that(
        client.get(handler),
        all_of(
            has_property("json", has_error_answer()),
            has_status(HTTPStatus.METHOD_NOT_ALLOWED)
        )
    )
