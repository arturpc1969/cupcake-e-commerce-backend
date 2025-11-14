from uuid import uuid4

import pytest
from django.contrib.auth import get_user_model
from django.test import Client

from accounts.utils import create_access_token
from api.models import Order, DeliveryAddress

User = get_user_model()


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def user():
    return User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="testpass123"
    )


@pytest.fixture
def staff_user():
    return User.objects.create_user(
        username="staffuser",
        email="staff@example.com",
        password="staffpass123",
        is_staff=True
    )


@pytest.fixture
def another_user():
    return User.objects.create_user(
        username="anotheruser",
        email="another@example.com",
        password="anotherpass123"
    )


@pytest.fixture
def delivery_address(user):
    return DeliveryAddress.objects.create(
        user=user,
        address_name="Minha casa",
        address_description="Rua Teste, 123",
        city="São Paulo",
        state="SP",
        zip_code="01234567"
    )


@pytest.fixture
def another_delivery_address(another_user):
    return DeliveryAddress.objects.create(
        user=another_user,
        address_name="Minha outra casa",
        address_description="Rua Outro, 456",
        city="Rio de Janeiro",
        state="RJ",
        zip_code="20000000"
    )


@pytest.fixture
def order(user, delivery_address):
    return Order.objects.create(
        user=user,
        delivery_address=delivery_address,
        payment_method=Order.PaymentMethod.PIX
    )


@pytest.fixture
def another_order(another_user, another_delivery_address):
    return Order.objects.create(
        user=another_user,
        delivery_address=another_delivery_address,
        payment_method=Order.PaymentMethod.CREDIT_CARD
    )


@pytest.fixture
def auth_headers(user):
    token = create_access_token(user.id)
    return {"HTTP_AUTHORIZATION": f"Bearer {token}"}


@pytest.fixture
def staff_auth_headers(staff_user):
    token = create_access_token(staff_user.id)
    return {"HTTP_AUTHORIZATION": f"Bearer {token}"}


# --- TESTES PARA LIST ORDERS ---

@pytest.mark.django_db
def test_list_orders_success(client, user, order, auth_headers):
    """Testa listagem de pedidos do usuário autenticado"""
    response = client.get("/api/orders/", **auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["uuid"] == str(order.uuid)
    assert data[0]["payment_method"] == order.payment_method


@pytest.mark.django_db
def test_list_orders_only_user_orders(client, user, another_user, order, another_order, auth_headers):
    """Testa que usuário só vê seus próprios pedidos"""
    response = client.get("/api/orders/", **auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["uuid"] == str(order.uuid)


@pytest.mark.django_db
def test_list_orders_without_auth(client):
    """Testa listagem sem autenticação"""
    response = client.get("/api/orders/")
    assert response.status_code == 401


# --- TESTES PARA LIST ORDERS STAFF ---

@pytest.mark.django_db
def test_list_orders_staff_success(client, order, another_order, staff_auth_headers):
    """Testa listagem de todos os pedidos para staff"""
    response = client.get("/api/orders/admin", **staff_auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    uuids = [item["uuid"] for item in data]
    assert str(order.uuid) in uuids
    assert str(another_order.uuid) in uuids


@pytest.mark.django_db
def test_list_orders_staff_forbidden_for_regular_user(client, auth_headers):
    """Testa que usuário comum não pode acessar rota de staff"""
    response = client.get("/api/orders/admin", **auth_headers)
    assert response.status_code == 403


# --- TESTES PARA GET ORDER ---

@pytest.mark.django_db
def test_get_order_success(client, user, order, auth_headers):
    """Testa busca de pedido específico"""
    response = client.get(f"/api/orders/{order.uuid}", **auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["uuid"] == str(order.uuid)
    assert data["payment_method"] == order.payment_method


@pytest.mark.django_db
def test_get_order_not_found(client, auth_headers):
    """Testa busca de pedido inexistente"""
    fake_uuid = uuid4()
    response = client.get(f"/api/orders/{fake_uuid}", **auth_headers)
    assert response.status_code == 404


@pytest.mark.django_db
def test_get_order_forbidden_other_user(client, another_order, auth_headers):
    """Testa que usuário não pode ver pedido de outro usuário"""
    response = client.get(f"/api/orders/{another_order.uuid}", **auth_headers)
    assert response.status_code == 404


# --- TESTES PARA GET ORDER STAFF ---

@pytest.mark.django_db
def test_get_order_staff_success(client, order, staff_auth_headers):
    """Testa busca de pedido específico para staff"""
    response = client.get(f"/api/orders/admin/{order.uuid}", **staff_auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["uuid"] == str(order.uuid)


@pytest.mark.django_db
def test_get_order_staff_forbidden_for_regular_user(client, order, auth_headers):
    """Testa que usuário comum não pode acessar rota de staff"""
    response = client.get(f"/api/orders/admin/{order.uuid}", **auth_headers)
    assert response.status_code == 403


# --- TESTES PARA CREATE ORDER ---

@pytest.mark.django_db
def test_create_order_success(client, user, delivery_address, auth_headers):
    """Testa criação de pedido com sucesso"""
    data = {
        "payment_method": "PIX",
        "delivery_address_uuid": str(delivery_address.uuid)
    }

    response = client.post(
        "/api/orders/",
        data=data,
        content_type="application/json",
        **auth_headers
    )

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["payment_method"] == "PIX"
    assert Order.objects.filter(user=user).count() == 1


@pytest.mark.django_db
def test_create_order_invalid_delivery_address(client, another_delivery_address, auth_headers):
    """Testa criação de pedido com endereço de outro usuário"""
    data = {
        "payment_method": "PIX",
        "delivery_address_uuid": str(another_delivery_address.uuid)
    }

    response = client.post(
        "/api/orders/",
        data=data,
        content_type="application/json",
        **auth_headers
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_create_order_invalid_payment_method(client, delivery_address, auth_headers):
    """Testa criação de pedido com método de pagamento inválido"""
    data = {
        "payment_method": "INVALID_METHOD",
        "delivery_address_uuid": str(delivery_address.uuid)
    }

    response = client.post(
        "/api/orders/",
        data=data,
        content_type="application/json",
        **auth_headers
    )

    assert response.status_code == 422


# --- TESTES PARA UPDATE ORDER STAFF ---

@pytest.mark.django_db
def test_update_order_staff_success(client, order, staff_auth_headers):
    """Testa atualização de pedido por staff"""
    data = {
        "payment_method": "PIX",
        "delivery_address_uuid": "ef624f70-95ca-479f-a27a-48c97f8cb22f",
        "status": "DELIVERED"
    }

    response = client.put(
        f"/api/orders/{order.uuid}",
        data=data,
        content_type="application/json",
        **staff_auth_headers
    )

    assert response.status_code == 200
    order.refresh_from_db()
    assert order.status == "DELIVERED"


@pytest.mark.django_db
def test_update_order_staff_forbidden_for_regular_user(client, order, auth_headers):
    """Testa que usuário comum não pode atualizar pedido"""
    data = {
        "payment_method": "PIX",
        "delivery_address_uuid": "ef624f70-95ca-479f-a27a-48c97f8cb22f",
        "status": "DELIVERED"
    }

    response = client.put(
        f"/api/orders/{order.uuid}",
        data=data,
        content_type="application/json",
        **auth_headers
    )

    assert response.status_code == 403


@pytest.mark.django_db
def test_update_order_staff_not_found(client, staff_auth_headers):
    """Testa atualização de pedido inexistente"""
    fake_uuid = uuid4()
    data = {
        "payment_method": "PIX",
        "delivery_address_uuid": "ef624f70-95ca-479f-a27a-48c97f8cb22f",
        "status": "DELIVERED"
    }

    response = client.put(
        f"/api/orders/{fake_uuid}",
        data=data,
        content_type="application/json",
        **staff_auth_headers
    )

    assert response.status_code == 404


# --- TESTES PARA UPDATE ORDER (USER CONFIRM) ---

@pytest.mark.django_db
def test_update_order_user_confirm_success(client, order, auth_headers):
    """Testa confirmação de pedido pelo usuário"""

    response = client.put(
        f"/api/orders/confirm/{order.uuid}",
        **auth_headers
    )

    assert response.status_code == 200
    order.refresh_from_db()
    assert order.status == "CONFIRMED"


@pytest.mark.django_db
def test_update_order_user_confirm_not_found(client, auth_headers):
    """Testa confirmação de pedido inexistente"""
    fake_uuid = uuid4()

    response = client.put(
        f"/api/orders/confirm/{fake_uuid}",
        **auth_headers
    )

    assert response.status_code == 404


# --- TESTES PARA DELETE ORDER STAFF ---

@pytest.mark.django_db
def test_delete_order_staff_success(client, order, staff_auth_headers):
    """Testa exclusão de pedido por staff"""
    response = client.delete(f"/api/orders/{order.uuid}", **staff_auth_headers)

    assert response.status_code == 204
    order.refresh_from_db()
    assert not order.is_active


@pytest.mark.django_db
def test_delete_order_staff_forbidden_for_regular_user(client, order, auth_headers):
    """Testa que usuário comum não pode excluir pedido"""
    response = client.delete(f"/api/orders/{order.uuid}", **auth_headers)
    assert response.status_code == 403


@pytest.mark.django_db
def test_delete_order_staff_not_found(client, staff_auth_headers):
    """Testa exclusão de pedido inexistente"""
    fake_uuid = uuid4()
    response = client.delete(f"/api/orders/{fake_uuid}", **staff_auth_headers)
    assert response.status_code == 404
