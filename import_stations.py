import csv

from db_helper import WeatherStation, get_session, WindDirection

"""there is a problem with this file, if the base is already created and inserted it will not work"""


def import_weather_stations():
    csvfile = open('weather_stations.csv', "rt", encoding='utf8')
    text = csv.reader(csvfile, delimiter=',')
    session = get_session()
    session = session()

    q = session.query(WeatherStation).all()
    if len(q) < 1:
        for row in text:
            w = WeatherStation()
            w.inmet_id = row[0]
            w.name = row[1]
            w.province = row[2]
            w.omm = row[3]

            session.add(w)

        session.commit()
        session.close()


def import_wind_directions():
    csvfile = open('wind_directions_codes.csv', "rt", encoding='utf8')
    text = csv.reader(csvfile, delimiter=',')
    session = get_session()
    session = session()

    q = session.query(WindDirection).all()
    if len(q) < 1:
        for row in text:
            wd = WindDirection()
            wd.id = row[0]
            wd.description = row[1]
            wd.initials = row[2]
            session.add(wd)

        session.commit()
        session.close()


def import_stations():
    import_weather_stations()
    import_wind_directions()
