import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://admin:admin123@172.20.10.2/health_monitoring'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MQTT_BROKER_URL = '127.0.0.1'  # or your broker IP
    MQTT_BROKER_PORT = 1883
    MQTT_KEEPALIVE = 60
    