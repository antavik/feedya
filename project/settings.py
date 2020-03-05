import os
import datetime

DB_URL = os.getenv('DATABASE_URL')

if DB_URL is None:
    DB_USERNAME = os.environ['DB_USERNAME']
    DB_PASSWORD = os.environ['DB_PASSWORD']
    DB_SERVER = os.environ['DB_SERVER']
    DB_DATABASE = os.environ['DB_DATABASE']

    DB_URL = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_SERVER}/{DB_DATABASE}'

SMPT_SERVER = os.getenv('SMPT_SERVER', 'smtp.gmail.com')
SMPT_SSL_PORT = os.getenv('SMPT_SSL_PORT', 465)
SENDER_EMAIL = os.environ['SENDER_EMAIL']
SENDER_EMAIL_PASSWORD = os.environ['SENDER_EMAIL_PASSWORD']
RECEIVER_EMAIL = os.environ['RECEIVER_EMAIL']

THREADS_QUANTITY = 4
THREAD_TIMEOUT = 20

TEMPLATES_DIR = './templates'
TEMPLATE_NAME = 'template.html'

TODAY_DATETIME = datetime.datetime.now()

MAX_LATE_NEWS = 3
