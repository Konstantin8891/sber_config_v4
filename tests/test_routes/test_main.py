import json

from fastapi import Depends
from sqlalchemy.orm import Session

import sys
sys.path.append("...")
# from models import Service, ServiceVersion, ServiceKey

from conftest import SessionTesting, app, db_session
from models import Service, ServiceKey, ServiceVersion
from schemas import CreateService, Key


def test_create_service(client):
    key = Key(service_key='testkey1', service_value='testvalue1')
    service = CreateService(
        name="testname1",
        version="testversion1",
        is_used=True,
        keys=[key, ]
    )
    # response = client.post("/create_service", json.dumps(data))
    # response = client.post("/create_service", service)
    # response = client.post("/create_service", params={"service": service.dict()})
    response = client.post("/create_service", json=service.dict())

    assert response.status_code == 201
    assert client.get(
        '/?service=testname1&version=testversion1'
    ).status_code == 200


def test_put_config(client):
    key = Key(service_key='testkey1', service_value='testvalue1')
    response = client.put('/', params={
        "service": "testname1",
        "version": "testversion1",
        "is_used": True,
        "keys": [key, ]
    })

    assert response.status_code == 200


def test_get_all(client):
    response = client.get('/get_all_services')
    assert response.status_code == 200
