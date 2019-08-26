from http import HTTPStatus

import pytest
from hamcrest import has_property, assert_that, all_of, has_entries, instance_of
from ..citizens.error_messages import ErrorMessages
from .matchers import has_status, has_error_answer


@pytest.mark.parametrize(
    "data",
    [
        {
            "citizens": [
                {
                    "citizen_id": 1,
                    "town": "dsa",
                    "street": "sadfa",
                    "building": "sadasd",
                    "apartment": 1,
                    "name": "sadasd",
                    "birth_date": "26.12.1926",
                    "gender": "male",
                    "relatives": [1]
                },
            ]
        },

        {
            "citizens": [
                {
                    "citizen_id": i,
                    "town": "dsa",
                    "street": "sadfa",
                    "building": "sadasd",
                    "apartment": 1,
                    "name": "sadasd",
                    "birth_date": "26.12.1926",
                    "gender": "male",
                    "relatives": [100 - 1 - i, i]
                } for i in range(100)
            ]
        }
    ]
)
def test_created_imports(client, data):
    assert_that(
        client.post("/imports", json=data),
        all_of(
            has_property("json", has_entries({"data": has_entries({"import_id": instance_of(int)})})),
            has_status(HTTPStatus.CREATED)
        )
    )


@pytest.mark.parametrize(
    ("data", "error_message"),
    [
        ("fsd", ErrorMessages.NOT_JSON_FORMAT),
        (['fdshg'], ErrorMessages.NOT_JSON_FORMAT),
        ({"citizens": [
            {
                "citizen_id": 1,
                "town": "dsa",
                "street": "sadfa"
            },
        ]}, ""),
        ({
            "citizens": [
                {
                    "citizen_id": 1,
                    "town": "dsa",
                    "street": "sadfa",
                    "building": "sadasd",
                    "apartment": 1,
                    "name": "sadasd",
                    "birth_date": "26.12.1926",
                    "gender": "male",
                    "relatives": []
                } for i in range(5)
            ]
        }, "")
    ]
)
def test_created_imports_wrong_data(client, data, error_message):
    assert_that(
        client.post("/imports", json=data),
        all_of(
            has_property("json", has_error_answer(error_message)),
            has_status(HTTPStatus.BAD_REQUEST)
        )
    )
