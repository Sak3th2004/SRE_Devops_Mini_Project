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


def test_ready():
    client = app.test_client()
    res = client.get("/ready")
    assert res.status_code == 200
    assert res.get_json()["status"] == "UP"


def test_info():
    client = app.test_client()
    res = client.get("/info")
    assert res.status_code == 200
    body = res.get_json()
    assert body["service"] == "system-health-dashboard"
    assert "uptime_seconds" in body


def test_slo():
    client = app.test_client()
    res = client.get("/slo")
    assert res.status_code == 200
    body = res.get_json()
    assert body["target"] == app.config["SLO_TARGET"]
    assert "availability_pct" in body
    assert "budget_remaining_pct" in body


def test_events():
    client = app.test_client()
    res = client.get("/events")
    assert res.status_code == 200
    assert "items" in res.get_json()


def test_deps_shape():
    client = app.test_client()
    res = client.get("/deps")
    assert res.status_code == 200
    body = res.get_json()
    assert "prometheus" in body
    assert "jenkins" in body
    assert "api" in body


def test_metrics_record_a_request():
    client = app.test_client()
    assert client.get("/health").status_code == 200
    body = client.get("/metrics").data.decode()
    assert "http_requests_total" in body
    assert 'path="/health"' in body
