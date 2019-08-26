# Анализ данных об житилях

[Задание](https://docviewer.yandex.ru/view/416117315/?*=K3i8NwnRdZXzGfsbhfQVy199ril7InVybCI6InlhLWRpc2stcHVibGljOi8vOHhSS3l5bXZVL0VsUGJCY3k1M3V1T043VEQzSEdrRU1TbGtEN0pXRWFweVFybTNadjhwVTRNMWJHL3RDRzlMSnEvSjZicG1SeU9Kb25UM1ZvWG5EYWc9PSIsInRpdGxlIjoiVEFTSy5wZGYiLCJub2lmcmFtZSI6ZmFsc2UsInVpZCI6IjQxNjExNzMxNSIsInRzIjoxNTY1MTYxMTIxMzE5LCJ5dSI6Ijg0MTA5NTMxMzE1NjQ2NjYxMTcifQ%3D%3D&nosw=1)

### Зависимости
Зависимости описаны в [`pyproject.toml`](web/pyproject.toml), можно посмотреть в красивом формате выполнив команду 
```
poetry show
```

### Запуск
Нужен `docker` и `docker-compose`

Установить переменные окружения, можно выполнив
```
cp env.sample .env
```
и установить в `.env` другие значения


Запуск докера 
```
docker-compose up
```

Запуск тестов

```
pytest
```