from pydantic import BaseModel
from datetime import date
from sqlalchemy import Column, String, Integer, Date, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class CapacityResponse(BaseModel):
    week_start_date: date
    week_no: int
    offered_capacity_teu: float


class Sailing(Base):
    __tablename__ = "sailings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ORIGIN = Column(String, nullable=False)
    DESTINATION = Column(String, nullable=False)
    SERVICE_VERSION_AND_ROUNDTRIP_IDENTFIERS = Column(String, nullable=False)
    ORIGIN_SERVICE_VERSION_AND_MASTER = Column(String, nullable=False)
    DESTINATION_SERVICE_VERSION_AND_MASTER = Column(String, nullable=False)
    ORIGIN_AT_UTC = Column(Date, nullable=False)
    OFFERED_CAPACITY_TEU = Column(Float, nullable=False)
