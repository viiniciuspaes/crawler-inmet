import csv

from sqlalchemy import Column, String, ForeignKey, Date, Interval, create_engine, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy_utils import database_exists, create_database

from config import DATABASE_URI, ID, WHEATHER_STATION, OMM, UTC_HOUR, DRY, WET, HUMIDITY, \
    PRESSURE_LEVEL, WIND_DIRECTION, WIND_SPEED, CLOUDNESS, DATE, INMET_ID, DESCRIPTION, INITIALS, NAME

Base = declarative_base()


class WeatherStation(Base):
    __tablename__ = 'weather_station'
    id = Column(Integer, primary_key=True)
    inmet_id = Column(INMET_ID, Integer)
    name = Column(NAME, String(255))
    # province = Column(PROVINCE, String(20), nullable=True)
    omm = Column(OMM, Integer)


class WindDirection(Base):
    __tablename__ = 'wind_direction'
    id = Column(ID, Integer, primary_key=True)
    description = Column(DESCRIPTION, String(32))
    initials = Column(INITIALS, String(20) )


class MeasurementsDaily(Base):
    __tablename__ = 'measurements_daily'
    id = Column(ID, Integer(), primary_key=True)
    weather_station_id = Column(WHEATHER_STATION, Integer, ForeignKey(WeatherStation.id), nullable=False)
    # measure_date_complete = Column(COMPLETE_DATE, DateTime)
    measure_date = Column(DATE, Date)
    utf_hour = Column(UTC_HOUR, Interval)
    temp_dry_bulb = Column(DRY, Float)
    temp_wet_bulb = Column(WET, Float)
    humidity = Column(HUMIDITY, Float)
    level_pressure_on_station = Column(PRESSURE_LEVEL, Float)
    wind_direction = Column(WIND_DIRECTION, Integer, ForeignKey(WindDirection.id), nullable=False)
    wind_speed = Column(WIND_SPEED, Float)
    cloudiness = Column(CLOUDNESS, Float)

    Weather_Station = relationship(WeatherStation, lazy='joined')
    Wind = relationship(WeatherStation, lazy='joined')



def get_engine():
    engine = create_engine(DATABASE_URI)
    return engine


def get_session():
    engine = get_engine()
    return sessionmaker(bind=engine,expire_on_commit=False)


def init():
    engine = get_engine()
    if not database_exists(engine.url):
        create_database(engine.url)
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine)




