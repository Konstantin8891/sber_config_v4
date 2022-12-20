import os
import sys

import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import models

from main import get_db, app
from database import Base
from schemas import Service, Key, PatchService


engine = create_engine(
    "sqlite:///./test_db.db",
    connect_args={"check_same_thread": False}
)
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(name="session")
def session_fixture():
    Base.metadata.create_all(engine)
    with SessionTesting(bind=engine.connect()) as db_session:
        yield db_session


@pytest.fixture(name="client")
def client_fixture(db_session: SessionTesting):
    def get_db_override():
        return db_session
    app.dependency_overrides[get_db] = get_db_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def create_service(
    service_name: str, is_used: bool, db_session: SessionTesting
):
    service_model = models.Service(name=service_name)
    db_session.add(service_model)
    db_session.commit()
    db_session.refresh(service_model)
    service_version_model = models.ServiceVersion(
        service_id=service_model.id,
        version='testversion2',
        is_used=is_used
    )
    db_session.add(service_version_model)
    db_session.commit()
    db_session.refresh(service_version_model)
    service_key_model = models.ServiceKey(
        service_id=service_model.id,
        version_id=service_version_model.id,
        service_key='key1',
        service_value='value1'
    )
    db_session.add(service_key_model)
    db_session.commit()


def test_create_service(client: TestClient):
    key = Key(service_key='testkey1', service_value='testvalue1')
    service = Service(
        name="testname1",
        version="testversion1",
        is_used=True,
        keys=[key, ]
    )
    response = client.post("/create_service", json=service.dict())
    assert response.status_code == 201
    assert client.get(
        '/?service=testname1&version=testversion1'
    ).status_code == 200


def test_put_config(client: TestClient):
    key = Key(service_key='testkey1', service_value='testvalue1')
    params = Service(
        name='testname2',
        version='testversion2',
        is_used=True,
        keys=[key]
    )
    response = client.put('/', content=params.json())
    assert response.status_code == 200
    assert client.get(
        '/?service=testname2&version=testversion2'
    ).status_code == 200


def test_get_current_service(db_session: SessionTesting, client: TestClient):
    service_name = 'testservice2'
    is_used = True
    create_service(service_name, is_used, db_session)
    assert client.get(
        '/?service=testservice2&version=testversion2'
    ).status_code == 200


def test_delete_service(db_session: SessionTesting, client: TestClient):
    is_used = False
    service_name = 'testservice2'
    create_service(service_name, is_used, db_session)
    response = client.delete(
        '/?service=testservice2&version=testversion2'
    )
    assert response.status_code == 204
    assert client.get(
        '/?service=testservice2&version=testversion2'
    ).status_code == 400
    is_used = True
    service_name = 'testservice3'
    create_service(service_name, is_used, db_session)
    response = client.delete(
        '/?service=testservice2&version=testversion2'
    )
    assert response.status_code == 400
    assert client.get(
        '/?service=testservice3&version=testversion2'
    ).status_code == 200


def test_patch_config(db_session: SessionTesting, client: TestClient):
    is_used = False
    service_name = 'testservice2'
    create_service(service_name, is_used, db_session)
    service = PatchService(
        name='testservice2',
        version='testversion2',
        is_used=True
    )
    response = client.patch('/', content=service.json())
    assert response.status_code == 206
    assert client.get(
        '/?service=testservice2&version=testversion2'
    ).json().get('is_used') is True
    service = PatchService(
        name='testservice2',
        version='testversion2',
        keys=[{'service_key': 'key1', 'service_value': 'value2'}]
    )
    response = client.patch('/', content=service.json())
    assert response.status_code == 206
    assert client.get(
        '/?service=testservice2&version=testversion2'
    ).json().get('keys') == {'key1': 'value2'}


def test_get_all(client: TestClient) -> None:
    response = client.get('/get_all_services')
    assert response.status_code == 200
