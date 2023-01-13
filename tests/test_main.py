import os
import sys

from typing import Generator

import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import models

from main import app
from database import Base
from routers.routers import get_db
from schemas import ServiceSchema, KeySchema


engine = create_engine(
    "sqlite:///./test_db.db",
    connect_args={"check_same_thread": False}
)
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(name="session")
def session_fixture() -> Generator[SessionTesting, None, None]:
    Base.metadata.create_all(engine)
    with SessionTesting(bind=engine.connect()) as session:
        yield session
    Base.metadata.drop_all(engine)


@pytest.fixture(name="client")
def client_fixture(session: SessionTesting) -> None:
    def get_db_override():
        return session
    app.dependency_overrides[get_db] = get_db_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def create_service(
    service_name: str, is_used: bool, session: SessionTesting
) -> None:
    service_model = models.Service(name=service_name)
    session.add(service_model)
    session.commit()
    session.refresh(service_model)
    service_version_model = models.ServiceVersion(
        service_id=service_model.id,
        version='testversion2',
        is_used=is_used
    )
    session.add(service_version_model)
    session.commit()
    session.refresh(service_version_model)
    service_key_model = models.ServiceKey(
        version_id=service_version_model.id,
        service_key='key1',
        service_value='value1'
    )
    session.add(service_key_model)
    session.commit()


def test_create_service(client: TestClient) -> None:
    key = KeySchema(service_key='testkey1', service_value='testvalue1')
    service = ServiceSchema(
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


def test_put_config(client: TestClient, session: SessionTesting) -> None:
    key = KeySchema(service_key='testkey1', service_value='testvalue1')
    service_name = 'testname1'
    is_used = True
    create_service(service_name, is_used, session)
    params = ServiceSchema(
        name='testname1',
        version='testversion2',
        is_used=False,
        keys=[key]
    )
    response = client.put('/', content=params.json())
    assert response.status_code == 200
    assert client.get(
        '/?service=testname1&version=testversion2'
    ).status_code == 200


def test_get_current_service(
    session: SessionTesting, client: TestClient
) -> None:
    service_name = 'testservice6'
    is_used = True
    create_service(service_name, is_used, session)
    assert client.get(
        '/?service=testservice6&version=testversion2'
    ).status_code == 200


def test_delete_service(session: SessionTesting, client: TestClient) -> None:
    is_used = False
    service_name = 'testservice3'
    create_service(service_name, is_used, session)
    response = client.delete(
        '/?service=testservice3&version=testversion2'
    )
    assert response.status_code == 204
    assert client.get(
        '/?service=testservice3&version=testversion2'
    ).status_code == 400
    is_used = True
    service_name = 'testservice4'
    create_service(service_name, is_used, session)
    response = client.delete(
        '/?service=testservice4&version=testversion2'
    )
    assert response.status_code == 400
    assert client.get(
        '/?service=testservice4&version=testversion2'
    ).status_code == 200


def test_get_all(client: TestClient) -> None:
    response = client.get('/get_all_services')
    assert response.status_code == 200
