from urllib.error import HTTPError, URLError
from urllib.request import urlopen


def probe(url, timeout=2):
    try:
        with urlopen(url, timeout=timeout) as resp:
            code = getattr(resp, "status", 200)
            return {"ok": True, "status": code}
    except HTTPError as err:
        return {"ok": err.code < 500, "status": err.code}
    except URLError as err:
        reason = err.reason if getattr(err, "reason", None) else err
        return {"ok": False, "error": str(reason)}
    except Exception as err:
        return {"ok": False, "error": str(err)}


def dependency_checks(app):
    prom = app.config["PROMETHEUS_URL"].rstrip("/")
    jenkins = app.config["JENKINS_URL"].rstrip("/")
    return {
        "process": {"ok": True, "status": 200},
        "prometheus": probe(prom + "/-/ready"),
        "jenkins": probe(jenkins + "/login"),
        "api": {"ok": True, "status": 200},
    }
