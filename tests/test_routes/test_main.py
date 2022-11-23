import json

from fastapi import Depends
from sqlalchemy.orm import Session

import sys
sys.path.append("...")
# from models import Service, ServiceVersion, ServiceKey
from conftest import get_db



# def test_create_service(client, db: Session = Depends(get_db)):
#     data = {
#         "name": "string",
#         "version": "string",
#         "is_used": True,
#         "keys": [{
#             "service_key": "string",
#             "service_value": "string"
#         }]
#     }
#     # response = client.post("/create_service", data)
#     response = client.post("/create_service")
#     assert response.status_code == 200
#     assert db.query(Service).filter(Service.name == 'string').exists() == True
#     assert db.query(ServiceVersion).filter(ServiceVersion.version == 'string').exists() == True
#     assert db.query(ServiceKey).filter(ServiceKey.service_key == 'string').exists() == True

def test_get_all(client, db: Session = Depends(get_db)):
    response = client.get('/get_all_services')
    assert response.status_code == 200

