import os


class Config:
    APP_ENV = os.environ.get("APP_ENV", "development")
    APP_VERSION = os.environ.get("APP_VERSION", "1.0.0")
    PORT = int(os.environ.get("PORT", "5000"))
    SLO_TARGET = float(os.environ.get("SLO_TARGET", "99.5"))
    PROMETHEUS_URL = os.environ.get("PROMETHEUS_URL", "http://43.205.104.60:9090")
    JENKINS_URL = os.environ.get("JENKINS_URL", "http://3.6.114.43:8080")
    K8S_NAMESPACE = os.environ.get("K8S_NAMESPACE", "student-11")
