import os


class Config:
    APP_ENV = os.environ.get("APP_ENV", "development")
    APP_VERSION = os.environ.get("APP_VERSION", "1.0.0")
    PORT = int(os.environ.get("PORT", "5000"))
