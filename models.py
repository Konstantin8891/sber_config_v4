from sqlalchemy import Integer, String, Boolean, ForeignKey, Column
from sqlalchemy.orm import relationship

from database import Base


class Service(Base):
    __tablename__ = 'service'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

    serviceversion = relationship(
        'ServiceVersion',
        back_populates='service',
        cascade='all, delete-orphan'
    )


class ServiceVersion(Base):
    __tablename__ = 'serviceversion'

    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey('service.id'))
    version = Column(String)
    is_used = Column(Boolean)

    service = relationship('Service', back_populates='serviceversion')
    servicekeys = relationship(
        'ServiceKey',
        back_populates='serviceversion',
        cascade='all, delete-orphan'
    )


class ServiceKey(Base):
    __tablename__ = 'servicekey'

    id = Column(Integer, primary_key=True, index=True)
    version_id = Column(Integer, ForeignKey('serviceversion.id'))
    service_key = Column(String)
    service_value = Column(String)

    serviceversion = relationship(
        'ServiceVersion', back_populates='servicekeys', passive_deletes=True
    )
