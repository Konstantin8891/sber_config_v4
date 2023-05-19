from typing import Generator, Union, Optional

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session, joinedload

from database import SessionLocal
from schemas import ServiceSchema

import models


router = APIRouter()


def get_db() -> Generator[SessionLocal, None, None]:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


async def get_keys_response(keys: models.ServiceKey) -> dict:
    response = {}
    for key in keys:
        response[key.service_key] = key.service_value
    return response


async def get_versions_response(
    versions: models.ServiceVersion,
    db: Session = Depends(get_db)
) -> dict:
    response_instance = [0] * versions.count()
    version_counter = 0
    for version in versions:
        response_instance[version_counter] = {}
        response_instance[version_counter][
            'version'
        ] = version.version
        response_instance[version_counter][
            'is_used'
        ] = version.is_used
        keys = db.query(models.ServiceKey).filter(
            models.ServiceKey.version_id == version.id
        )
        response_instance[version_counter]['keys'] = await get_keys_response(keys)
        version_counter += 1
    return response_instance


async def get_version_response(
    version: models.ServiceVersion,
    db: Session = Depends(get_db)
):
    response_instance = []
    response_instance.append({})
    response_instance[0]['version'] = version.version
    response_instance[0]['is_used'] = version.is_used
    keys = db.query(models.ServiceKey).filter(
        models.ServiceKey.version_id == version.id
    )
    response_instance[0]['keys'] = await get_keys_response(keys)
    return response_instance


async def get_service(
    service_name: str, db: Session = Depends(get_db)
) -> Union[models.Service, None]:
    return db.query(models.Service).filter(
        models.Service.name == service_name
    ).first()


async def get_service_version(
    service_version: str, service_id: int, db: Session = Depends(get_db)
) -> Union[models.ServiceVersion, None]:
    return db.query(models.ServiceVersion).filter(
        models.ServiceVersion.version == service_version
    ).filter(models.ServiceVersion.service_id == service_id).first()


@router.post('/create_service', status_code=status.HTTP_201_CREATED)
async def post_service(
    service: ServiceSchema, db: Session = Depends(get_db)
) -> Union[str, Exception]:
    service_instance = await get_service(service.name, db)
    if service_instance is None:
        service_instance = models.Service(name=service.name)
        db.add(service_instance)
        db.commit()
        db.refresh(service_instance)
    serviceversion_model = models.ServiceVersion()
    serviceversion_instance = db.query(models.ServiceVersion).filter(
        models.ServiceVersion.service_id == service_instance.id
    ).filter(models.ServiceVersion.version == service.version).first()
    if serviceversion_instance:
        raise HTTPException(
            status_code=400, detail='Version of service already exists'
        )
    serviceversion_model.version = service.version
    serviceversion_model.is_used = service.is_used
    serviceversion_model.service_id = service_instance.id
    db.add(serviceversion_model)
    db.commit()
    db.refresh(serviceversion_model)
    for key in service.keys:
        servicekey_model = models.ServiceKey(
            version_id=serviceversion_model.id,
            service_key=key.service_key,
            service_value=key.service_value
        )
        db.add(servicekey_model)
        db.commit()
    response = {}
    response['service'] = service.name
    response['versions'] = await get_version_response(serviceversion_model, db)
    return response


@router.get('/get_all_services')
async def get_all(db: Session = Depends(get_db)) -> list:
    return db.query(models.Service).order_by(models.Service.id).options(
        joinedload(models.Service.serviceversion).joinedload(
            models.ServiceVersion.servicekeys
        )
    ).all()


@router.get('/')
async def get_current_service(
    service: str,
    db: Session = Depends(get_db),
    version: Optional[str] = None
) -> dict:
    service_instance = await get_service(service, db)
    if service_instance is None:
        raise HTTPException(status_code=400, detail='Service does not exist')
    response_instance = {}
    if not version:
        versions = db.query(models.ServiceVersion).filter(
            models.ServiceVersion.service_id == service_instance.id
        )
        response_instance['service'] = service_instance.name
        response_instance['versions'] = await get_versions_response(
            versions, db
        )
        return response_instance
    else:
        service_version = await get_service_version(version, service_instance.id, db)
        if service_version is None:
            raise HTTPException(
                status_code=400, detail='version does not exist'
            )
        response_instance['service'] = service
        response_instance['versions'] = await get_version_response(
            service_version, db
        )
        return response_instance


# @router.put(
#     '/',
#     responses={
#         status.HTTP_200_OK: {'response': 'OK'},
#         status.HTTP_201_CREATED: {'response': 'Created'}
#     }
# )
@router.put('/')
async def put_config(
    create_service: ServiceSchema,
    db: Session = Depends(get_db)
) -> str:
    service_instance = await get_service(create_service.name, db)
    if service_instance is None:
        raise HTTPException(status_code=400, detail='service does not exist')
    version_instance = await get_service_version(
        create_service.version, service_instance.id, db
    )
    if version_instance is None:
        raise HTTPException(status_code=400, detail='version does not exist')
    if version_instance.is_used != create_service.is_used:
        version_instance.is_used = create_service.is_used
        db.commit()
        db.refresh(version_instance)
    db.query(models.ServiceKey).filter(
        models.ServiceKey.version_id == version_instance.id
    ).delete()
    service_key_instance = [0] * len(create_service.keys)
    servicekey_counter = 0
    for key in create_service.keys:
        service_key_instance[servicekey_counter] = models.ServiceKey()
        service_key_instance[
            servicekey_counter
        ].version_id = version_instance.id
        service_key_instance[servicekey_counter].service_key = key.service_key
        service_key_instance[
            servicekey_counter
        ].service_value = key.service_value
        db.add(service_key_instance[servicekey_counter])
        db.commit()
        servicekey_counter += 1
    response_instance = {}
    response_instance['service'] = create_service.name
    response_instance['versions'] = await get_version_response(
        version_instance, db
    )
    return response_instance


@router.delete('/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_config(
    service: str, version: str, db: Session = Depends(get_db)
) -> str:
    service_instance = db.query(models.Service).filter(
        models.Service.name == service
    ).first()
    if service_instance is None:
        raise HTTPException(status_code=400, detail='Service not found')
    version_instance = db.query(models.ServiceVersion).filter(
        models.ServiceVersion.service_id == service_instance.id
    ).filter(models.ServiceVersion.version == version).first()
    if version_instance is None:
        raise HTTPException(
            status_code=400, detail='Version of service not found'
        )
    if version_instance.is_used:
        raise HTTPException(status_code=400, detail='Config is in use')
    db.query(models.ServiceKey).filter(
        models.ServiceKey.version_id == version_instance.id
    ).delete()
    db.query(models.ServiceVersion).filter(
        models.ServiceVersion.version == version
    ).delete()
    db.commit()
    return 'deleted'
