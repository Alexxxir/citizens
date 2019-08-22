import os


class Config:
    DEBUG = False
    POSTGRES_URL = os.environ.get("POSTGRES_URL", "db:5432")
    POSTGRES_USER = os.environ.get("POSTGRES_USER", 'postgres')
    POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", '')
    POSTGRES_DB = os.environ.get("POSTGRES_DB", '')
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_URL}/{POSTGRES_DB}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    DEVELOPMENT = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
