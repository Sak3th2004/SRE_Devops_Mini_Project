from app import app


def test_health_returns_up():
    client = app.test_client()
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json()["status"] == "UP"


def test_version_is_present():
    client = app.test_client()
    res = client.get("/version")
    assert res.status_code == 200
    body = res.get_json()
    assert "version" in body
    assert body["version"]


def test_environment_comes_from_config():
    client = app.test_client()
    res = client.get("/environment")
    assert res.status_code == 200
    body = res.get_json()
    assert "environment" in body
    assert body["environment"] == app.config["APP_ENV"]
