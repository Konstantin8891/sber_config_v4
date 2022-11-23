from sqlalchemy import Integer, String, Boolean, ForeignKey, Column
from sqlalchemy.orm import relationship

from database import Base

class Service(Base):
    __tablename__ = 'service'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

    serviceversion = relationship("ServiceVersion", back_populates='service_v')
    servicekey = relationship('ServiceKey', back_populates='service')


class ServiceVersion(Base):
    __tablename__ = 'serviceversion'

    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey('service.id'))
    version = Column(String)
    is_used = Column(Boolean)
    
    service_v = relationship('Service', back_populates='serviceversion')
    servicekeyversion = relationship('ServiceKey', back_populates='serviceversion')


class ServiceKey(Base):
    __tablename__ = 'servicekey'

    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey('service.id'))
    version_id = Column(Integer, ForeignKey('serviceversion.id'))
    service_key = Column(String)
    service_value = Column(String)

    service = relationship('Service', back_populates='servicekey')
    serviceversion = relationship('ServiceVersion', back_populates='servicekeyversion')
