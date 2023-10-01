from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Material(Base):
    __tablename__ = 'material'
    id = Column(Integer, primary_key=True)
    itemcode = Column(String)
    description = Column(String)
    unit = Column(String)

class Transaction(Base):
    __tablename__ = 'transaction'
    id = Column(Integer, primary_key=True)
    material_id = Column(Integer, ForeignKey('material.id'))
    material = relationship(Material)
    trans_type = Column(String)
    quantity = Column(Float)
    price = Column(Float)
    trans_date = Column(DateTime)
    remarks = Column(String)
