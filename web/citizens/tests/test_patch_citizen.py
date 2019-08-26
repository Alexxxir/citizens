from http import HTTPStatus

import pytest
from hamcrest import has_property, equal_to, assert_that, all_of, has_entries

from .matchers import has_status
from .some_testing_data import add_citizen


@pytest.mark.parametrize(
    "data",
    [
        {
            "name": "Новое имя",
        }
    ]
)
def test_patch_citizens(client, data):
    import_id = add_citizen(client)
    assert_that(
        client.patch(f"/imports/{import_id}/citizens/1", json=data),
        all_of(
            has_property("json", has_entries({"data": has_entries({"name": equal_to(data["name"])})})),
            has_status(HTTPStatus.OK)
        )
    )
