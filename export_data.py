import csv

from config import STATION_ID
from db_helper import get_session, MeasurementsDaily


def export_data():
    session = get_session()
    session = session()

    q = session.query(MeasurementsDaily).filter_by(weather_station_id=STATION_ID)

    query_list = q
    # mds = q.all()
    f = open('climate_data_daily_conventional_brasil.csv', "w")
    writer = csv.writer(f, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)

    first_row = [
        u" ID ",
        u" Weather Station ",
        u" OMM Weather Station ",
        u" Province ",
        u" Complete Date ",
        u" Date ",
        u" UTC Hour ",
        u" Temp dry bulb ",
        u" temp wet bulb ",
        u" Humidity ",
        u" Level Pressure on Station ",
        u" Wind Direction ",
        u" Desc Wind Direction ",
        u" Wind Speed ",
        u" Cloudiness "
    ]

    writer.writerow(first_row)

    for d in query_list:
        r = []
        r.append(d.id)
        r.append(d.name)
        r.append(d.omm)
        # r.append(d.province)
        # r.append(d.measure_date_complete)
        r.append(d.measure_date)
        r.append(d.utf_hour)
        r.append(d.temp_dry_bulb)
        r.append(d.temp_wet_bulb)
        r.append(d.level_pressure_on_station)
        r.append(d.wind_direction)
        r.append(d.Wind.description)
        r.append(d.wind_speed)
        r.append(d.cloudiness)

        writer.writerow(r)

    f.close()
    session.close()
