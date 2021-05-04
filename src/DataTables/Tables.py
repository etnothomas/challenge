from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, func, Text, Numeric
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class GlobalCapacities(Base):

    __tablename__ = 'global_capacities'

    id = Column(Integer, primary_key=True, autoincrement=True)
    supplier = Column(String)
    capacity = Column(Integer)


class RegionalCapacities(Base):

    __tablename__ = 'regional_capacities'

    id = Column(Integer, primary_key=True, autoincrement=True)
    country_supplier = Column(String)
    region = Column(String)
    country_destination = Column(String)
    type = Column(String)
    supplier = Column(String)
    capacity = Column(Integer)


class Offers(Base):

    __tablename__ = 'offers'

    item = Column(String, primary_key=True)
    supplier = Column(String, primary_key=True)
    unit_price = Column(Numeric)
    project_id = Column(String, nullable=False, primary_key=True)
    capacity = Column(Integer, nullable=True)



