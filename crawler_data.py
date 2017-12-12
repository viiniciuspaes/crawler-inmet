import logging
import sys
import time
from datetime import datetime, timedelta

from bs4 import BeautifulSoup
from selenium import webdriver

from config import USER, PASS, LOGIN_URL
from db_helper import get_session, WeatherStation, MeasurementsDaily
from utils import datestring_to_date


def login():
    browser = webdriver.PhantomJS()
    browser.get(LOGIN_URL)
    email_element = browser.find_element_by_name("mCod")
    email_element.send_keys(USER)
    time.sleep(1)
    pass_element = browser.find_element_by_name("mSenha")
    pass_element.send_keys(PASS)
    time.sleep(1)
    pass_element.submit()
    return browser


def crawl_data():
    logging.basicConfig(filename='crawler.log', level=logging.INFO)

    browser = login()
    session = get_session()
    session = session()

    ws = session.query(WeatherStation).all()

    for w in ws:

        logging.info('{} {}: Crawling... '.format(w.omm, w.name))

        start = "01/01/1961"
        end = datetime.now() - timedelta(days=90)
        end = end.strftime("%d/%m/%Y")
        code_ws = str(w.omm)

        url = "http://www.inmet.gov.br/projetos/rede/pesquisa/gera_serie_txt.php?&mRelEstacao=" + \
              code_ws + "&btnProcesso=serie&mRelDtInicio=" + start + "&mRelDtFim=" + \
              end + "&mAtributos=1,1,,,1,1,,1,1,,,1,,,,,"

        browser.get(url)
        soup = BeautifulSoup(browser.page_source, "html.parser")

        try:
            for pre in soup.find('pre'):
                rows = pre.string.splitlines()
                for r in rows:
                    if r.startswith(code_ws):

                        try:
                            dt = datestring_to_date(r.split(';')[1])
                        except ValueError:
                            dt = None

                        try:
                            hour_utc = r.split(';')[2]
                            hour = int(int(hour_utc) / 100)
                            hour_utc_td = timedelta(hours=hour)
                        except ValueError:
                            hour_utc_td = None

                        hour_utc = r.split(';')[2]
                        hour = int(int(hour_utc) / 100)
                        dt_complete = datetime(year=dt.year, month=dt.month, day=dt.day, hour=hour)

                        try:
                            db = float(r.split(';')[3])
                        except ValueError:
                            db = None

                        try:
                            wb = float(r.split(';')[4])
                        except ValueError:
                            wb = None

                        try:
                            h = float(r.split(';')[5])
                        except ValueError:
                            h = None

                        try:
                            p = float(r.split(';')[6])
                        except ValueError:
                            p = None

                        try:
                            wd = int(r.split(';')[7])
                        except ValueError:
                            wd = 0

                        try:
                            ws = float(r.split(';')[8])
                        except ValueError:
                            ws = None

                        try:
                            c = int(r.split(';')[9])
                        except ValueError:
                            c = None

                        try:
                            md = MeasurementsDaily()
                            md.weather_station_id = w.id
                            md.measure_date_complete = dt_complete
                            md.measure_date = dt
                            md.utf_hour = hour_utc_td
                            md.temp_dry_bulb = db
                            md.temp_wet_bulb = wb
                            md.humidity = h
                            md.level_pressure_on_station = p
                            md.wind_direction = wd
                            md.wind_speed = ws
                            md.cloudiness = c

                            session.add(md)

                        except:
                            logging.info(r)
                            logging.info(sys.exc_info()[0])

                session.commit()
                session.close()

        except TypeError:
            logging.info('{} {}: End of this stations ...  '.format(w.omm, w.name))
            logging.info('Html:{}'.format(soup.prettify()))

        logging.info('{} {}: End of this station ...  '.format(w.omm, w.name))
