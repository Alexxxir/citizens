import os


class Config:
    DEBUG = False
    POSTGRES_URL = os.environ.get("POSTGRES_URL", "db:5432")
    POSTGRES_USER = os.environ.get("POSTGRES_USER", "dev")
    POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "12345")
    POSTGRES_DB = os.environ.get("POSTGRES_DB", "dev")
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_URL}/{POSTGRES_DB}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DEBUG = False
    POSTGRES_DB = os.environ.get("POSTGRES_DB", "test")


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
