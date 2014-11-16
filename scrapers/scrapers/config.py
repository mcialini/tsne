from sys import platform as _platform
import logging
import requests
import psycopg2

if _platform == "win32" or _platform == "win64":
    files_store = 'D:/Dropbox/Town Square New England/scraped/'
else:
    files_store = '/home/matt/Dropbox/Town Square New England/scraped/'

imgmagick = 'C:\Program Files\ImageMagick-6.8.9-Q16\convert'

directory = {
    'madoi': 'MA_DOI/',
    'madob': 'MA_DOB/',
    'masos': 'MA_SOS/',
    'medoi': 'ME_DOI/',
    'nhdoi': 'NH_DOI/',
    'ridoi': 'RI_DOI/',
    'vtdfr': 'VT_DFR/',
    'vtdoi': 'VT_DOI/',
    'ctdoimed': 'CT_DOI_MED/'
}

with open('scrape.log', "w"):
    pass

logging.basicConfig(
    filename='scrape.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

s = requests.Session()

conn = psycopg2.connect(
    host='104.131.36.242', dbname='django', user='django', password='xDxhU01Wd3')
dbcur = conn.cursor()
