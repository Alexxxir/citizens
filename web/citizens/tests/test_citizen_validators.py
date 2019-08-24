import pytest
from ..citizens.models import Citizen
from hamcrest import assert_that, calling, is_not, raises


@pytest.mark.parametrize(
    "citizen_id",
    [
        "dsaf", "1432", "", None, -1, [], 7.2
    ],
)
def test_wrong_citizen_id(citizen_id):
    assert_that(calling(Citizen).with_args(citizen_id=citizen_id), raises(ValueError))


@pytest.mark.parametrize(
    "citizen_id",
    [
        0, 1, 12, 190,
    ],
)
def test_correct_citizen_id(citizen_id):
    assert_that(calling(Citizen).with_args(citizen_id=citizen_id), is_not(raises(ValueError)))


@pytest.mark.parametrize(
    "town",
    [
        "", 1, [], True, "---", "s" * 257
    ],
)
def test_wrong_town(town):
    assert_that(calling(Citizen).with_args(town=town), raises(ValueError))


@pytest.mark.parametrize(
    "town",
    [
        "d", "1----", "----1", "----f----", "a" * 256
    ],
)
def test_correct_town(town):
    assert_that(calling(Citizen).with_args(town=town), is_not(raises(ValueError)))


@pytest.mark.parametrize(
    "street",
    [
        "", 1, [], True, "---", "s" * 257
    ],
)
def test_wrong_street(street):
    assert_that(calling(Citizen).with_args(street=street), raises(ValueError))


@pytest.mark.parametrize(
    "street",
    [
        "d", "1----", "----1", "----f----", "a" * 256
    ],
)
def test_correct_street(street):
    assert_that(calling(Citizen).with_args(street=street), is_not(raises(ValueError)))


@pytest.mark.parametrize(
    "building",
    [
        "", 1, [], True, "---", "s" * 257
    ],
)
def test_wrong_building(building):
    assert_that(calling(Citizen).with_args(building=building), raises(ValueError))


@pytest.mark.parametrize(
    "building",
    [
        "d", "1----", "----1", "----f----", "a" * 256
    ],
)
def test_correct_building(building):
    assert_that(calling(Citizen).with_args(building=building), is_not(raises(ValueError)))


@pytest.mark.parametrize(
    "apartment",
    [
        "dsaf", "1432", "", None, -1, [], 7.2
    ],
)
def test_wrong_apartment(apartment):
    assert_that(calling(Citizen).with_args(apartment=apartment), raises(ValueError))


@pytest.mark.parametrize(
    "apartment",
    [
        0, 1, 12, 190,
    ],
)
def test_correct_apartment(apartment):
    assert_that(calling(Citizen).with_args(apartment=apartment), is_not(raises(ValueError)))


@pytest.mark.parametrize(
    "name",
    [
        "", 1, [], True, "s" * 257, None
    ],
)
def test_wrong_name(name):
    assert_that(calling(Citizen).with_args(name=name), raises(ValueError))


@pytest.mark.parametrize(
    "name",
    [
        "d", "---", "1----", "----1", "----f----", "a" * 256
    ],
)
def test_correct_name(name):
    assert_that(calling(Citizen).with_args(name=name), is_not(raises(ValueError)))


@pytest.mark.parametrize(
    "birth_date",
    [
        "", "15 марта", "05-11-1998", "1998.11.05",  # неправильный формат
        "32.01.1998", ".01.1998", "00.01.1998", "das.01.1998", "31.02.1998", "31.11.1998"  # неправильный день
        "05.00.1998", "05.13.1998", "05.312.1998", "05.3d.1998",  # неправильный месяц
        "05.11.1", "05.11.19198", "05.11.11", "05.11.0",  # неправильный год
        "05.11.3000"  # больше текущей даты
    ],
)
def test_wrong_birth_date(birth_date):
    assert_that(calling(Citizen).with_args(birth_date=birth_date), raises(ValueError))


@pytest.mark.parametrize(
    "birth_date",
    [
        "05.11.1998", "29.02.2000", "31.01.2010"
    ],
)
def test_correct_birth_date(birth_date):
    assert_that(calling(Citizen).with_args(birth_date=birth_date), is_not(raises(ValueError)))


@pytest.mark.parametrize(
    "gender",
    [
        "", 1, [], True, "s" * 257, None
    ],
)
def test_wrong_gender(gender):
    assert_that(calling(Citizen).with_args(gender=gender), raises(ValueError))


@pytest.mark.parametrize(
    "gender",
    [
        "male", "female"
    ],
)
def test_correct_gender(gender):
    assert_that(calling(Citizen).with_args(gender=gender), is_not(raises(ValueError)))
