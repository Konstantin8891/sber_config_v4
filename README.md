# English description is below

# sber_config_v4

# API для просмотра, изменения, добавления конфигов приложений

API поддерживает версионирование

## Стек

python 3.10

FastAPI 0.87

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

# API for getting, changing, adding configuration of services

API supports versioning

## Stack

python 3.10

FastAPI 0.87

Alembic 1.8.1

SQLAlchemy 1.4.44

Pytest 7.2.0

## Running the project

git clone git@github.com:Konstantin8891/sber_config_v4.git

docker-compose up --build

## Requests

POST

http://localhost:8000/create_service

Create version of configuration

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

Get all information about all services

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

Create or edit version of configuration

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

Edit version of configuration

DELETE

http://localhost:8000/?service=managed-k11s&version=1.0

Delete unused version of configuration
