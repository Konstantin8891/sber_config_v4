import json

from fastapi import Depends
from sqlalchemy.orm import Session

import sys
sys.path.append("...")
# from models import Service, ServiceVersion, ServiceKey

from conftest import SessionTesting, app, db_session
from models import Service, ServiceKey, ServiceVersion
from schemas import CreateService, Key


# def test_create_service(client, db: Session = Depends(get_db)):
def test_create_service(client):
    data = {
        "name": "string",
        "version": "string",
        "is_used": True,
        "keys": [{
            "service_key": "string",
            "service_value": "string"
        }]
    }
    # db = client.get_db()
    key = Key(service_key='testkey1', service_value='testvalue1')
    service = CreateService(
        name="testname1",
        version="testversion1",
        is_used=True,
        keys=[key, ]
    )
    # response = client.post("/create_service", json.dumps(data))
    # response = client.post("/create_service", service)
    # print(service.dict())
    # response = client.post("/create_service", params={"service": service.dict()})
    response = client.post("/create_service", json=service.dict())

    assert response.status_code == 201
    assert db.query(Service).filter(Service.name == 'testname1').exists() is True
    assert db.query(ServiceVersion).filter(ServiceVersion.version == 'testversion1').exists() is True
    assert db.query(ServiceKey).filter(ServiceKey.service_key == 'testkey1').exists() is True
    
 

def test_get_all(client):
    response = client.get('/get_all_services')
    assert response.status_code == 200
