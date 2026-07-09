# config.py
import os

class Config:
    DEBUG = False
    TESTING = False
    EDGAR_IDENTITY = os.environ.get("EDGAR_IDENTITY")

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False