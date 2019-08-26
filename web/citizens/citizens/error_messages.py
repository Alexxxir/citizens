class ErrorMessages:
    INCORRECT_DATA_FORMAT = "Неверный формат данных"
    INCORRECT_RELATIVES = "Неверно указаны связи"
    NOT_FOUND_CITIZEN = "Житель не найден"
    NOT_JSON_FORMAT = "Данные должны быть в формате json"
    NOT_FOUND_IMPORT = "Не найдена выгрузка с жителями"


class ErrorFieldsMessages:
    INCORRECT_FIELDS = "Указаны неверные поля"
    INCORRECT_ADDRESS = "Город, улица и дом - строка, содержащая хотя бы 1 букву или цифру, не более 256 символов"
    INCORRECT_DATA_FORMAT = "Дата рождения должна быть в формате ДД.ММ.ГГГГ"
    INCORRECT_BIRTH_DATA = "Дата рождения должна быть меньше текущей даты"
    INCORRECT_APARTMENT = "apartment - целое неотрицательное число"
    INCORRECT_NAME = "name - непустая строка, не более 256 символов"
    INCORRECT_GENDER = "gender - male или female"
    INCORRECT_CITIZEN_ID = "citizen_id - целое неотрицательное число"
