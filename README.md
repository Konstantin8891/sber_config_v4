# English description is below

# sber_config_v4

# API для просмотра, изменения, добавления конфигов приложений

API поддерживает версионирование

## Стек

python 3.10

FastAPi 0.87

Alembic 1.8.1

SQLAlchemy 1.4.44

Pytest 7.2.0

## Инструкция по запуску

git clone git@github.com:Konstantin8891/sber_config_v4.git

docker-compose up --build

## Примеры запросов

POST

http://localhost:8000/create_service

Создание версии конфига

{
  "name": "string",
  "version": "string",
  "is_used": true,
  "keys": [
    {
      "service_key": "string",
      "service_value": "string"
    }
  ]
}

GET

http://localhost:8000/get_all_services

Выводит всю информацию обо всех сервисах

[
  {
    "service": "testservise1",
    "versions": [
      {
        "version": "testversion1",
        "is_used": true,
        "keys": {
          "key1": "value2"
        }
      }
    ]
  },
  {
    "service": "testservice1",
    "versions": []
  }
]

GET

http://localhost:8000/?service=name_of_service&version=version

Выводит все ключи и значения версии сервиса, либо если версия не указана, то информацию обо всех версиях сервиса

PUT

curl -X 'PUT' \
  'http://localhost:8000/?service=managed-k11s&version=1.0&is_used=true' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '[
  {
    "service_key": "key1",
    "service_value": "value1"
  }
]'

Создаёт или редактирует версию сервиса

PATCH

curl -X 'PATCH' \
  'http://localhost:8000/?service=managed-k11s&version=1.0&is_used=true' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '[
  {
    "service_key": "string",
    "service_value": "string"
  }
]'

Редактирует версию конфигурации

DELETE

http://localhost:8000/?service=managed-k11s&version=1.0

Удаляет неиспользуемую версию конфигурации

# API for viewing, changing, adding configuration of services
