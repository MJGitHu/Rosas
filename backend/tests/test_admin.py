from datetime import datetime

import pytest
from werkzeug.security import generate_password_hash

from app import create_app
from app.routes import admin as admin_routes


class TestConfig:
    SECRET_KEY = "a" * 64
    DEBUG = False
    ADMIN_USERNAME = "administradora"
    ADMIN_PASSWORD_HASH = generate_password_hash("admin-password")
    SESSION_COOKIE_SECURE = False
    FRONTEND_ORIGINS = []


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr("app.init_db_pool", lambda: None)
    monkeypatch.setattr("app.close_db_pool", lambda: None)
    monkeypatch.setattr(admin_routes, "login_attempts", {})
    application = create_app(TestConfig)
    application.config.update(TESTING=True)
    return application.test_client()


def sign_in(client):
    return client.post(
        "/api/admin/login",
        json={"username": "administradora", "password": "admin-password"},
    )


def test_admin_contract_endpoints_require_login(client):
    assert client.get("/api/admin/reservas?mes=2026-10").status_code == 401
    assert client.get("/api/reservas/").status_code == 401


def test_login_sets_session_and_logout_requires_csrf(client):
    response = sign_in(client)
    assert response.status_code == 200
    csrf_token = response.json["csrf_token"]

    session_response = client.get("/api/admin/session")
    assert session_response.json["authenticated"] is True
    assert session_response.json["csrf_token"] == csrf_token

    assert client.post("/api/admin/logout").status_code == 403
    logout_response = client.post(
        "/api/admin/logout",
        headers={"X-CSRF-Token": csrf_token},
    )
    assert logout_response.status_code == 200
    assert client.get("/api/admin/session").json["authenticated"] is False


def test_login_rejects_invalid_credentials(client):
    response = client.post(
        "/api/admin/login",
        json={"username": "administradora", "password": "incorrect"},
    )
    assert response.status_code == 401
    assert response.json["message"] == "Usuario o contraseña incorrectos."


def test_login_is_disabled_when_admin_credentials_are_not_configured(client):
    client.application.config.update(ADMIN_USERNAME="", ADMIN_PASSWORD_HASH="")
    response = sign_in(client)
    assert response.status_code == 503
    assert response.json["message"] == "La administración no está configurada en el servidor."


def test_login_rate_limits_repeated_failures(client):
    for _ in range(admin_routes.MAX_LOGIN_ATTEMPTS):
        response = client.post(
            "/api/admin/login",
            json={"username": "administradora", "password": "incorrect"},
        )
        assert response.status_code == 401

    response = sign_in(client)
    assert response.status_code == 429


def test_calendar_validates_month_and_reports_database_unavailable(client, monkeypatch):
    sign_in(client)
    monkeypatch.setattr(admin_routes, "get_db_connection", lambda: None)

    assert client.get("/api/admin/reservas?mes=2026-13").status_code == 400
    assert client.get("/api/admin/reservas?mes=9999-12").status_code == 400
    response = client.get("/api/admin/reservas?mes=2026-10")
    assert response.status_code == 503
    assert "datos de ejemplo" in response.json["message"]


def test_calendar_queries_and_serializes_reservations(client, monkeypatch):
    class FakeCursor:
        parameters = None

        def __enter__(self):
            return self

        def __exit__(self, *args):
            assert len(args) == 3
            return False

        def execute(self, query, **parameters):
            assert "FROM eventos_reservas" in query
            self.parameters = parameters

        def fetchall(self):
            return [(
                "RS-2026-001",
                "Elena",
                "Gómez",
                "999123456",
                "elena@example.test",
                "Mariachi completo",
                datetime(2026, 10, 15),
                "18:30",
                1.5,
                "Av. Ejemplo 123",
                "Cumpleaños",
                "COTIZADA",
                680,
                0,
                680,
                340,
                340,
                "Repertorio especial",
                "TRANSFERENCIA",
            )]

    class FakeConnection:
        cursor_instance = FakeCursor()

        def cursor(self):
            return self.cursor_instance

        def close(self):
            pass

    connection = FakeConnection()
    monkeypatch.setattr(admin_routes, "get_db_connection", lambda: connection)
    sign_in(client)

    response = client.get("/api/admin/reservas?mes=2026-10")
    assert response.status_code == 200
    assert response.json["data"][0]["codigo_reserva"] == "RS-2026-001"
    assert response.json["data"][0]["detalles"] == "Repertorio especial"
    assert connection.cursor_instance.parameters == {
        "start_date": datetime(2026, 10, 1),
        "end_date": datetime(2026, 11, 1),
    }


def test_flask_serves_the_frontend_from_same_origin(client):
    assert client.get("/").status_code == 200
    assert client.get("/frontend/src/css/styles.css").status_code == 200
