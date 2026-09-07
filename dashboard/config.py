import os


class Config:
    APP_ENV = os.environ.get("APP_ENV", "development")
<<<<<<< HEAD
    APP_VERSION = os.environ.get("APP_VERSION", "1.0.0-dev")
=======
    APP_VERSION = os.environ.get("APP_VERSION", "1.0.1")
>>>>>>> feature/version-note
    PORT = int(os.environ.get("PORT", "5000"))
