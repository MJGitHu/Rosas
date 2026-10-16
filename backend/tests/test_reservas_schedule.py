from datetime import date, datetime, timedelta

import pytest
from werkzeug.security import generate_password_hash

from app import create_app
from app.routes import reservas as reservas_routes


class TestConfig:
    SECRET_KEY = "b" * 64
    DEBUG = False
    ADMIN_USERNAME = "administradora"
    ADMIN_PASSWORD_HASH = generate_password_hash("admin-password")
    SESSION_COOKIE_SECURE = False
    FRONTEND_ORIGINS = []


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr("app.init_db_pool", lambda: None)
    monkeypatch.setattr("app.close_db_pool", lambda: None)
    application = create_app(TestConfig)
    application.config.update(TESTING=True)
    return application.test_client()


def test_schedule_allows_opening_hours_including_overnight():
    event_date = (date.today() + timedelta(days=1)).isoformat()

    assert reservas_routes._parse_schedule(event_date, "11:00", 30)[1] == 30
    assert reservas_routes._parse_schedule(event_date, "01:00", 60)[1] == 60
    assert reservas_routes._parse_schedule(event_date, "00:30", 40)[1] == 40


@pytest.mark.parametrize("event_time", ["01:15", "10:59", "02:00"])
def test_schedule_rejects_times_outside_opening_hours(event_time):
    event_date = (date.today() + timedelta(days=1)).isoformat()
    with pytest.raises(ValueError, match="11:00 y la 01:00"):
        reservas_routes._parse_schedule(event_date, event_time, 30)


def test_schedule_rejects_extra_durations():
    event_date = (date.today() + timedelta(days=1)).isoformat()
    with pytest.raises(ValueError, match="duración"):
        reservas_routes._parse_schedule(event_date, "14:00", 120)


def test_schedule_conflict_uses_event_duration_and_45_minute_gap():
    class Cursor:
        def __init__(self, rows):
            self.rows = rows
            self.parameters = None

        def execute(self, _query, **parameters):
            self.query = _query
            self.parameters = parameters

        def fetchall(self):
            return self.rows

    event_day = date.today() + timedelta(days=1)
    existing_event = (datetime.combine(event_day, datetime.min.time()), "14:00", 1)

    cursor = Cursor([existing_event])
    assert reservas_routes._find_schedule_conflict(
        cursor, datetime.combine(event_day, datetime.strptime("15:44", "%H:%M").time()), 30
    )
    assert not reservas_routes._find_schedule_conflict(
        cursor, datetime.combine(event_day, datetime.strptime("15:45", "%H:%M").time()), 30
    )
    assert cursor.parameters["start_date"].date() == event_day - timedelta(days=1)
    assert cursor.parameters["end_date"].date() == event_day + timedelta(days=2)
    assert "estado_reserva <> 'CANCELADA'" in cursor.query


def test_40_minute_contract_keeps_exact_duration_when_stored_as_decimal_hours():
    class Cursor:
        def execute(self, *_args, **_parameters):
            pass

        def fetchall(self):
            return [(datetime(2026, 10, 20), "14:00", 0.67)]

    event_day = date(2026, 10, 20)
    cursor = Cursor()
    assert reservas_routes._find_schedule_conflict(
        cursor, datetime.combine(event_day, datetime.strptime("15:24", "%H:%M").time()), 30
    )
    assert not reservas_routes._find_schedule_conflict(
        cursor, datetime.combine(event_day, datetime.strptime("15:25", "%H:%M").time()), 30
    )


def test_schedule_conflict_includes_the_previous_calendar_day():
    event_day = date.today() + timedelta(days=1)
    cursor = type(
        "Cursor",
        (),
        {
            "execute": lambda self, *_args, **_kwargs: None,
            "fetchall": lambda self: [
                (datetime.combine(event_day - timedelta(days=1), datetime.min.time()), "23:30", 1)
            ],
        },
    )()

    assert reservas_routes._find_schedule_conflict(
        cursor, datetime.combine(event_day, datetime.strptime("01:00", "%H:%M").time()), 30
    )


def test_availability_endpoint_returns_conflict_without_exposing_contract(client, monkeypatch):
    event_day = date.today() + timedelta(days=1)

    class Cursor:
        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return False

        def execute(self, _query, **_parameters):
            pass

        def fetchall(self):
            return [(datetime.combine(event_day, datetime.min.time()), "14:00", 1)]

    class Connection:
        def cursor(self):
            return Cursor()

        def close(self):
            pass

    monkeypatch.setattr(reservas_routes, "get_db_connection", Connection)
    response = client.get(
        f"/api/reservas/disponibilidad?fecha={event_day.isoformat()}&hora=15%3A00&duracion_minutos=30"
    )

    assert response.status_code == 200
    assert response.json["available"] is False
    assert "codigo_reserva" not in response.json


def test_public_reservation_endpoint_rejects_invalid_schedule_before_database(client, monkeypatch):
    def unexpected_database_access():
        raise AssertionError("La reserva inválida no debe acceder a la base de datos.")

    monkeypatch.setattr(reservas_routes, "get_db_connection", unexpected_database_access)
    event_day = (date.today() + timedelta(days=1)).isoformat()
    response = client.post(
        "/api/reservas/",
        json={
            "cliente": {
                "nombre": "Elena",
                "apellido": "Gómez",
                "telefono": "999123456",
                "email": "elena@example.test",
            },
            "servicio": "mariachi",
            "duracion_minutos": 30,
            "direccion_evento": "Av. Ejemplo 123",
            "fecha_evento": event_day,
            "hora_evento": "02:00",
        },
    )

    assert response.status_code == 400
    assert "11:00 y la 01:00" in response.json["message"]


def test_public_reservation_saves_pending_contract_with_server_price(client, monkeypatch):
    event_day = date.today() + timedelta(days=1)
    statements = []

    class Cursor:
        rowcount = 1

        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return False

        def execute(self, query, **parameters):
            statements.append((query, parameters))
            self.query = query

        def fetchall(self):
            return []

        def fetchone(self):
            if "SELECT id_formato" in self.query:
                return (7,)
            if "SELECT id_zona" in self.query:
                return (8,)
            if "SELECT id_cliente" in self.query:
                return (9,)
            return None

    class Connection:
        def cursor(self):
            return Cursor()

        def commit(self):
            self.did_commit = True

        def rollback(self):
            self.did_rollback = True

        def close(self):
            pass

    connection = Connection()
    monkeypatch.setattr(reservas_routes, "get_db_connection", lambda: connection)
    response = client.post(
        "/api/reservas/",
        json={
            "cliente": {
                "nombre": "Elena",
                "apellido": "Gómez",
                "telefono": "999123456",
                "email": "elena@example.test",
            },
            "servicio": "mariachi",
            "duracion_minutos": 30,
            "direccion_evento": "Av. Ejemplo 123",
            "fecha_evento": event_day.isoformat(),
            "hora_evento": "14:00",
            "detalles": "Confirmar repertorio",
            "monto_total": 1,
            "metodo_pago": "PRUEBA",
        },
    )

    assert response.status_code == 201
    assert response.json["data"]["estado"] == "COTIZADA"
    assert response.json["data"]["monto_total"] == 380
    assert response.json["data"]["anticipo_requerido"] == 190
    insert, parameters = next(
        entry for entry in statements if "INSERT INTO eventos_reservas" in entry[0]
    )
    assert "'COTIZADA'" in insert
    assert "'PENDIENTE'" in insert
    assert parameters["monto_total"] == 380
    assert parameters["anticipo_requerido"] == 190
    assert connection.did_commit
