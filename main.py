from typing import Optional

from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

import models

from database import SessionLocal
from schemas import CreateService, Key

app = FastAPI()


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_keys_response(keys: models.ServiceKey):
    response = {}
    for key in keys:
        response[key.service_key] = key.service_value
    return response


def get_versions_response(
    versions: models.ServiceVersion,
    service_instance: models.Service,
    db: Session = Depends(get_db)
):
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
            models.ServiceKey.service_id == service_instance.id
        ).filter(models.ServiceKey.version_id == version.id)
        response_instance[version_counter]['keys'] = get_keys_response(keys)
        version_counter += 1
    return response_instance

@app.post('/create_service', status_code=status.HTTP_201_CREATED)
async def post_service(
    response: Response, service: CreateService, db: Session = Depends(get_db)
):
    service_model = models.Service()
    service_name = service.name
    service_instance = db.query(models.Service).filter(
        models.Service.name == service_name
    ).first()
    if service_instance is None:
        service_model.name = service_name
        db.add(service_model)
        db.commit()
    serviceversion_model = models.ServiceVersion()
    service_instance = db.query(models.Service).filter(
        models.Service.name == service_name
    ).first()
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
    service_dict = service.dict()
    for key in list(service_dict):
        if isinstance(service_dict[key], list):
            sub_dicts = service_dict[key]
    if not sub_dicts:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return HTTPException(status_code=400, detail='No keys in config')

    servicekey_models = []
    for i in range(len(sub_dicts)):
        servicekey_model = models.ServiceKey()
        servicekey_models.append(servicekey_model)
        servicekey_models[i].service_id = service_instance.id
        servicekey_models[i].version_id = serviceversion_model.id
        servicekey_models[i].service_key = sub_dicts[i].get('service_key')
        servicekey_models[i].service_value = sub_dicts[i].get('service_value')
        db.add(servicekey_models[i])
        db.commit()
    return 'created'

@app.get('/get_all_services')
async def get_all(db: Session = Depends(get_db)):
    service_counter = 0
    services = db.query(models.Service).all()
    model = models.Service()
    response = [0] * len(services)
    for service in services:
        response[service_counter] = {}
        response[service_counter]['service'] = service.name
        versions = db.query(models.ServiceVersion).filter(
            models.ServiceVersion.service_id == service.id
        )
        response[service_counter]['versions'] = get_versions_response(
            versions, service, db
        )
        service_counter +=1
    return response

@app.get('/')
async def get_current_service(
    service: str,
    response: Response,
    db: Session = Depends(get_db),
    version: Optional[str] = None
):
    service_instance = db.query(models.Service).filter(
        models.Service.name == service
    ).first()
    if service_instance is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return HTTPException(status_code=400, detail='Service does not exist')
    response_instance = {}
    if not version:
        versions = db.query(models.ServiceVersion).filter(
            models.ServiceVersion.service_id == service_instance.id
        )
        response_instance['service'] = service_instance.name
        response_instance['versions'] = get_versions_response(
            versions, service_instance, db
        )
        return response_instance
    else:
        service_version = db.query(models.ServiceVersion).filter(
            models.ServiceVersion.version == version
        ).first()
        if service_version is None:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return HTTPException(
                status_code=400, detail='version does not exist'
            )
        response_instance['service'] = service
        response_instance['version'] = version
        keys = db.query(models.ServiceKey).filter(
            models.ServiceKey.service_id == service_instance.id
        ).filter(models.ServiceKey.version_id == service_version.id)
        response_instance['keys'] = get_keys_response(keys)
        return response_instance

@app.put('/')
async def put_config(service: str, version: str, is_used: bool, keys: list[Key], response: Response, db: Session = Depends(get_db)):
    service_instance = db.query(models.Service).filter(models.Service.name == service).first()
    if service_instance is None:
        service_instance = models.Service()
        service_instance.name = service
        db.add(service_instance)
        db.commit()
    service_instance = db.query(models.Service).filter(models.Service.name == service).first()
    version_instance = db.query(models.ServiceVersion).filter(models.ServiceVersion.service_id == service_instance.id).filter(models.ServiceVersion.version == version).first()
    if version_instance is None:
        version_instance = models.ServiceVersion()
        version_instance.service_id = service_instance.id
        version_instance.version = version
        version_instance.is_used = is_used
        db.add(version_instance)
        db.commit()
        db.refresh(version_instance)
    db.query(models.ServiceKey).filter(models.ServiceKey.service_id == service_instance.id).filter(models.ServiceKey.version_id == version_instance.id).delete()
    service_key_instance = [0] * len(keys)
    servicekey_counter = 0
    for key in keys:
        service_key_instance[servicekey_counter] = models.ServiceKey()
        service_key_instance[servicekey_counter].service_id = service_instance.id
        service_key_instance[servicekey_counter].version_id = version_instance.id
        service_key_instance[servicekey_counter].service_key = key.service_key
        service_key_instance[servicekey_counter].service_value = key.service_value
        db.add(service_key_instance[servicekey_counter])
        db.commit()
        servicekey_counter += 1
    return 'put'

@app.patch('/', status_code=status.HTTP_206_PARTIAL_CONTENT)
async def patch_config(
    service: str,
    version: str,
    is_used: Optional[bool] = None,
    keys: Optional[list[Key]] = None,
    db: Session = Depends(get_db)
):
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
    if is_used is not None:
        if version_instance.is_used != is_used:
            version_instance.is_used = is_used
            db.commit()
    if keys is not None:
        for key in keys:
            servicekey_instance = db.query(models.ServiceKey).filter(
                models.ServiceKey.service_id == service_instance.id
            ).filter(
                models.ServiceKey.version_id == version_instance.id
            ).filter(models.ServiceKey.service_key == key.service_key).first()
            if servicekey_instance is None:
                servicekey_model = models.ServiceKey()
                servicekey_model.service_id = service_instance.id
                servicekey_model.version_id = version_instance.id
                servicekey_model.service_key = key.service_key
                servicekey_model.service_value = key.service_value
                db.add(servicekey_model)
                db.commit()
            if servicekey_instance.service_value != key.service_value:
                servicekey_instance.service_id = service_instance.id
                servicekey_instance.version_id = version_instance.id
                servicekey_instance.service_key = key.service_key
                servicekey_instance.service_value = key.service_value
                db.commit()
    return 'patched'

@app.delete('/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_config(service: str, version: str, db: Session = Depends(get_db)):
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
    if version_instance.is_used == True:
        raise HTTPException(status_code=400, detail='Config is in use')
    db.query(models.ServiceKey).filter(
        models.ServiceKey.service_id == service_instance.id
    ).filter(models.ServiceKey.version_id == version_instance.id).delete()
    db.query(models.ServiceVersion).filter(
        models.ServiceVersion.service_id == service_instance.id
    ).filter(models.ServiceVersion.version == version).delete()
    db.commit()
    return 'deleted'
