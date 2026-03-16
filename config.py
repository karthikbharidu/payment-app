from dotenv import load_dotenv
import os

load_dotenv()

class Config:

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICCATIONS = False