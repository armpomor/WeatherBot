"""
Models database
"""

from sqlalchemy import Column, Integer, String, DateTime, BigInteger, Float, Time
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class
    """
    pass


class Person(Base):
    """
    Table with user settings.
    Table with the fields below
    The primary_key=True parameter specifies whether
    that this column will represent the primary key.
    The index=True parameter says that for the given column
    an index will be created.
    """
    __tablename__ = 'people'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger)
    name = Column(String)
    language = Column(String)
    coordinates = Column(String)


class WeatherHistory(Base):
    """
    The table in which the bot will save
    the weather every day on schedule.
    """
    __tablename__ = 'weather'
    id = Column(Integer, primary_key=True, index=True)
    date_time = Column(DateTime)
    sunrise = Column(Time)
    sunset = Column(Time)
    long_day = Column(String)
    condition = Column(String)
    precipitation = Column(Integer)
    temp_max = Column(Integer)
    temp_min = Column(Integer)
    wind_mps = Column(Float)
    humidity = Column(Integer)
    pressure = Column(Integer)
    cloud = Column(Integer)
    air_co = Column(Float)
    air_no2 = Column(Float)
    air_o3 = Column(Float)
    air_so2 = Column(Float)
    air_pm2_5 = Column(Float)
    air_pm10 = Column(Float)
