import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///health_monitoring.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MQTT_BROKER_URL = 'localhost'  # or your broker IP
    MQTT_BROKER_PORT = 1883
    MQTT_KEEPALIVE = 60
    