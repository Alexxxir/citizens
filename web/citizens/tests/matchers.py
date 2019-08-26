from hamcrest import has_property, equal_to, has_entries, not_none


def has_status(status: int):
    return has_property('status_code', equal_to(status))


def has_error_answer(answer: str = ""):
    return has_entries(
        {
            "error": has_entries({"message": not_none() if not answer else equal_to(answer)})
        }
    )
