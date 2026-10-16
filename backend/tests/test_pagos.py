import hashlib
import hmac
import json
from datetime import date, timedelta
from decimal import Decimal

import pytest
from werkzeug.security import generate_password_hash

from app import create_app
from app.config.payment_methods import get_comision
from app.routes import pagos as pagos_routes
from app.services.calculator_service import calcular_cotizacion


class TestConfig:
    SECRET_KEY = "c" * 64
    DEBUG = False
    ADMIN_USERNAME = "administradora"
    ADMIN_PASSWORD_HASH = generate_password_hash("admin-password")
    SESSION_COOKIE_SECURE = False
    FRONTEND_ORIGINS = []
    MERCADOPAGO_ACCESS_TOKEN = "test-access-token"
    MERCADOPAGO_WEBHOOK_URL = "https://example.test/api/pagos/webhook"
    MERCADOPAGO_WEBHOOK_SECRET = "test-webhook-secret"


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr("app.init_db_pool", lambda: None)
    monkeypatch.setattr("app.close_db_pool", lambda: None)
    application = create_app(TestConfig)
    application.config.update(TESTING=True)
    return application.test_client()


def make_contract(method="MERCADOPAGO"):
    return {
        "cliente": {
            "nombre": "Elena",
            "apellido": "Gómez",
            "telefono": "999123456",
            "email": "elena@example.test",
        },
        "servicio": "mariachi",
        "duracion_minutos": 40,
        "direccion_evento": "Av. Ejemplo 123",
        "fecha_evento": (date.today() + timedelta(days=3)).isoformat(),
        "hora_evento": "14:00",
        "detalles": "Prueba de pago",
        "metodo_pago": method,
    }


def test_trial_quote_is_one_sol_for_the_full_contract():
    quote = calcular_cotizacion(680, 1, metodo_pago="PRUEBA", monto_base_formato=680)

    assert quote["monto_total_evento"] == 1.0
    assert quote["anticipo_50_requerido"] == 1.0
    assert quote["saldo_50_restante"] == 0.0
    assert quote["total_a_pagar_hoy"] == 1.0
    assert get_comision("PRUEBA") == 0.0


def test_contract_uses_server_catalog_price_and_trial_amount():
    normal = pagos_routes._validate_contract(make_contract())
    trial = pagos_routes._validate_contract(make_contract("PRUEBA"))

    assert normal[4] == Decimal("480.00")
    assert normal[5] == Decimal("240.00")
    assert trial[4] == Decimal("1.00")
    assert trial[5] == Decimal("1.00")
    assert trial[6] == Decimal("0.00")


def test_preference_rejects_invalid_payment_method_before_database_or_provider(client, monkeypatch):
    def unexpected_call(*_args, **_kwargs):
        raise AssertionError("No debe contactar Oracle ni Mercado Pago.")

    monkeypatch.setattr(pagos_routes, "get_db_connection", unexpected_call)
    monkeypatch.setattr(pagos_routes, "_mercado_pago_request", unexpected_call)

    response = client.post(
        "/api/pagos/preferencias",
        json=make_contract("TRANSFERENCIA"),
    )

    assert response.status_code == 400
    assert "método de pago válido" in response.json["message"]


@pytest.mark.parametrize(
    ("method", "expected_amount", "expected_total"),
    [
        ("MERCADOPAGO", 240.0, Decimal("480.00")),
        ("PRUEBA", 1.0, Decimal("1.00")),
    ],
)
def test_preference_uses_server_price_and_holds_slot(
    client,
    monkeypatch,
    method,
    expected_amount,
    expected_total,
):
    class Cursor:
        def __init__(self):
            self.executed = []

        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return False

        def execute(self, query, **parameters):
            self.executed.append((query, parameters))

        def fetchall(self):
            return []

    class Connection:
        def __init__(self):
            self.test_cursor = Cursor()
            self.did_commit = False
            self.did_close = False

        def cursor(self):
            return self.test_cursor

        def commit(self):
            self.did_commit = True

        def rollback(self):
            raise AssertionError("No se esperaba rollback.")

        def close(self):
            self.did_close = True

    connections = []

    def new_connection():
        connection = Connection()
        connections.append(connection)
        return connection

    provider_payloads = []

    def create_preference(method, path, payload, idempotency_key):
        provider_payloads.append((method, path, payload, idempotency_key))
        return {
            "id": "preference-123",
            "init_point": "https://www.mercadopago.com.pe/checkout/redirect",
        }

    monkeypatch.setattr(pagos_routes, "_database_connection", new_connection)
    monkeypatch.setattr(pagos_routes, "_mercado_pago_request", create_preference)
    monkeypatch.setattr(pagos_routes, "_set_intent_status", lambda *_args, **_kwargs: None)

    body = make_contract(method)
    body["monto_total"] = 99999
    response = client.post("/api/pagos/preferencias", json=body)

    assert response.status_code == 201
    assert response.json["data"]["monto_a_pagar"] == expected_amount
    assert provider_payloads[0][2]["items"][0]["unit_price"] == expected_amount
    assert provider_payloads[0][2]["external_reference"] == response.json["data"]["referencia_externa"]
    insert = next(
        parameters
        for query, parameters in connections[0].test_cursor.executed
        if "INSERT INTO mercadopago_intents" in query
    )
    assert insert["monto_total"] == expected_total
    assert insert["monto_pago"] == Decimal(str(expected_amount))
    assert any(
        "LOCK TABLE eventos_reservas IN EXCLUSIVE MODE" in query
        for query, _ in connections[0].test_cursor.executed
    )
    assert connections[0].did_commit


def test_webhook_rejects_invalid_signature_without_fetching_payment(client, monkeypatch):
    def unexpected_call(*_args, **_kwargs):
        raise AssertionError("Un webhook inválido no debe consultar el pago.")

    monkeypatch.setattr(pagos_routes, "_mercado_pago_request", unexpected_call)
    response = client.post(
        "/api/pagos/webhook",
        json={"type": "payment", "data": {"id": "12345"}},
        headers={"x-signature": "ts=123,v1=invalid", "x-request-id": "request-1"},
    )

    assert response.status_code == 401


def test_webhook_rejects_non_object_payload(client):
    response = client.post(
        "/api/pagos/webhook?topic=payment",
        data="[]",
        content_type="application/json",
    )

    assert response.status_code == 401


def test_expected_webhook_alias_accepts_post_and_acknowledges_merchant_order(client):
    response = client.post(
        "/api/webhooks/mercadopago?id=12345&topic=merchant_order",
    )

    assert response.status_code == 200
    assert response.json == {"status": "ignored"}


def test_expected_webhook_alias_rejects_get(client):
    response = client.get("/api/webhooks/mercadopago")

    assert response.status_code == 405


def test_rejected_attempt_keeps_checkout_retryable(client, monkeypatch):
    payment_id = "12345"
    request_id = "request-2"
    timestamp = "1704908010"
    manifest = f"id:{payment_id};request-id:{request_id};ts:{timestamp};"
    digest = hmac.new(
        TestConfig.MERCADOPAGO_WEBHOOK_SECRET.encode(),
        manifest.encode(),
        hashlib.sha256,
    ).hexdigest()
    monkeypatch.setattr(
        pagos_routes,
        "_mercado_pago_request",
        lambda *_args, **_kwargs: {"status": "rejected"},
    )
    monkeypatch.setattr(
        pagos_routes,
        "get_db_connection",
        lambda: pytest.fail("Un intento rechazado no debe cerrar el intento de checkout."),
    )

    response = client.post(
        "/api/pagos/webhook?type=payment&data.id=12345",
        json={"type": "payment", "data": {"id": payment_id}},
        headers={
            "x-signature": f"ts={timestamp},v1={digest}",
            "x-request-id": request_id,
        },
    )

    assert response.status_code == 200


def test_webhook_signature_uses_payment_id_request_id_and_timestamp(app_context):
    payment_id = "12345"
    request_id = "request-1"
    timestamp = "1704908010"
    manifest = f"id:{payment_id};request-id:{request_id};ts:{timestamp};"
    digest = hmac.new(
        TestConfig.MERCADOPAGO_WEBHOOK_SECRET.encode(),
        manifest.encode(),
        hashlib.sha256,
    ).hexdigest()
    with app_context.test_request_context(
        "/api/pagos/webhook",
        headers={
            "x-signature": f"ts={timestamp},v1={digest}",
            "x-request-id": request_id,
        },
    ):
        assert pagos_routes._valid_webhook_signature(payment_id)


@pytest.fixture
def app_context(monkeypatch):
    monkeypatch.setattr("app.init_db_pool", lambda: None)
    monkeypatch.setattr("app.close_db_pool", lambda: None)
    application = create_app(TestConfig)
    with application.app_context():
        yield application


class _Cursor:
    def __init__(self, intent_state="PENDIENTE", paid_amount=Decimal("240.00")):
        self.intent_state = intent_state
        self.paid_amount = paid_amount
        self.last_query = ""
        self.executed = []

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def execute(self, query, **parameters):
        self.last_query = query
        self.executed.append((query, parameters))

    def fetchone(self):
        if "SELECT contrato_json" in self.last_query:
            contract = json.dumps(make_contract())
            return (contract, Decimal("480.00"), self.paid_amount, self.intent_state)
        if "SELECT id_formato" in self.last_query:
            return (7,)
        if "SELECT id_zona" in self.last_query:
            return (8,)
        if "SELECT id_cliente" in self.last_query:
            return (9,)
        if "SELECT id_reserva" in self.last_query:
            return (10,)
        return None

    def fetchall(self):
        return []


class _Connection:
    def __init__(self, cursor):
        self.test_cursor = cursor
        self.did_commit = False
        self.did_rollback = False
        self.did_close = False

    def cursor(self):
        return self.test_cursor

    def commit(self):
        self.did_commit = True

    def rollback(self):
        self.did_rollback = True

    def close(self):
        self.did_close = True


def test_approved_webhook_persists_reservation_and_payment_once(app_context, monkeypatch):
    cursor = _Cursor()
    connection = _Connection(cursor)
    monkeypatch.setattr(pagos_routes, "get_db_connection", lambda: connection)
    payment = {
        "status": "approved",
        "external_reference": "12345678-1234-1234-1234-123456789012",
        "transaction_amount": "240.00",
        "currency_id": "PEN",
    }

    with app_context.test_request_context("/"):
        pagos_routes._persist_approved_payment(
            payment,
            payment_id="987654321",
        )

    statements = [query for query, _ in cursor.executed]
    assert any(
        "INSERT INTO eventos_reservas" in query and "'ANTICIPO_PAGADO'" in query
        for query in statements
    )
    assert any("INSERT INTO pagos" in query for query in statements)
    assert any("SET estado = 'APROBADO'" in query for query in statements)
    assert connection.did_commit


def test_duplicate_approved_webhook_does_not_create_another_reservation(app_context, monkeypatch):
    cursor = _Cursor(intent_state="APROBADO")
    connection = _Connection(cursor)
    monkeypatch.setattr(pagos_routes, "get_db_connection", lambda: connection)

    with app_context.test_request_context("/"):
        pagos_routes._persist_approved_payment(
            {
                "status": "approved",
                "external_reference": "12345678-1234-1234-1234-123456789012",
                "transaction_amount": "240.00",
                "currency_id": "PEN",
            },
            payment_id="987654321",
        )

    assert not any(
        "INSERT INTO eventos_reservas" in query
        for query, _ in cursor.executed
    )
    assert connection.did_commit
