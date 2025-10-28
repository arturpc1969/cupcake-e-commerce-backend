from uuid import uuid4

import pytest
from django.contrib.auth import get_user_model
from django.test import Client

from accounts.utils import create_access_token
from api.models import DeliveryAddress

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
        address_name="Minha Casa",
        address_description="Rua Teste, 123",
        city="São Paulo",
        state="SP",
        zip_code="01234567"
    )


@pytest.fixture
def another_delivery_address(another_user):
    return DeliveryAddress.objects.create(
        user=another_user,
        address_name="Casa do Outro",
        address_description="Rua Outro, 456",
        city="Rio de Janeiro",
        state="RJ",
        zip_code="20000000"
    )


@pytest.fixture
def auth_headers(user):
    token = create_access_token(user.id)
    return {"HTTP_AUTHORIZATION": f"Bearer {token}"}


@pytest.fixture
def staff_auth_headers(staff_user):
    token = create_access_token(staff_user.id)
    return {"HTTP_AUTHORIZATION": f"Bearer {token}"}


# --- TESTES PARA LIST DELIVERY ADDRESSES ---

@pytest.mark.django_db
def test_list_delivery_addresses_success(client, user, delivery_address, auth_headers):
    """Testa listagem de endereços do usuário autenticado"""
    response = client.get("/api/delivery-addresses/", **auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["uuid"] == str(delivery_address.uuid)
    assert data[0]["address_name"] == delivery_address.address_name


@pytest.mark.django_db
def test_list_delivery_addresses_only_user_addresses(client, user, another_user, delivery_address,
                                                     another_delivery_address, auth_headers):
    """Testa que usuário só vê seus próprios endereços"""
    response = client.get("/api/delivery-addresses/", **auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["uuid"] == str(delivery_address.uuid)


@pytest.mark.django_db
def test_list_delivery_addresses_staff_sees_all(client, delivery_address, another_delivery_address, staff_auth_headers):
    """Testa que staff vê todos os endereços"""
    response = client.get("/api/delivery-addresses/", **staff_auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    uuids = [item["uuid"] for item in data]
    assert str(delivery_address.uuid) in uuids
    assert str(another_delivery_address.uuid) in uuids


@pytest.mark.django_db
def test_list_delivery_addresses_empty(client, auth_headers):
    """Testa listagem quando não há endereços"""
    response = client.get("/api/delivery-addresses/", **auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0


@pytest.mark.django_db
def test_list_delivery_addresses_without_auth(client):
    """Testa listagem sem autenticação"""
    response = client.get("/api/delivery-addresses/")
    assert response.status_code == 401


# --- TESTES PARA GET DELIVERY ADDRESS ---

@pytest.mark.django_db
def test_get_delivery_address_success(client, user, delivery_address, auth_headers):
    """Testa busca de endereço específico"""
    response = client.get(f"/api/delivery-addresses/{delivery_address.uuid}", **auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["uuid"] == str(delivery_address.uuid)
    assert data["address_name"] == delivery_address.address_name
    assert data["city"] == delivery_address.city


@pytest.mark.django_db
def test_get_delivery_address_not_found(client, auth_headers):
    """Testa busca de endereço inexistente"""
    fake_uuid = uuid4()
    response = client.get(f"/api/delivery-addresses/{fake_uuid}", **auth_headers)
    assert response.status_code == 404


@pytest.mark.django_db
def test_get_delivery_address_forbidden_other_user(client, another_delivery_address, auth_headers):
    """Testa que usuário não pode ver endereço de outro usuário"""
    response = client.get(f"/api/delivery-addresses/{another_delivery_address.uuid}", **auth_headers)
    assert response.status_code == 403


@pytest.mark.django_db
def test_get_delivery_address_staff_can_see_any(client, another_delivery_address, staff_auth_headers):
    """Testa que staff pode ver qualquer endereço"""
    response = client.get(f"/api/delivery-addresses/{another_delivery_address.uuid}", **staff_auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["uuid"] == str(another_delivery_address.uuid)


@pytest.mark.django_db
def test_get_delivery_address_without_auth(client, delivery_address):
    """Testa busca sem autenticação"""
    response = client.get(f"/api/delivery-addresses/{delivery_address.uuid}")
    assert response.status_code == 401


# --- TESTES PARA CREATE DELIVERY ADDRESS ---

@pytest.mark.django_db
def test_create_delivery_address_success(client, user, auth_headers):
    """Testa criação de endereço com sucesso"""
    data = {
        "address_name": "Meu Trabalho",
        "address_description": "Av. Paulista, 1000",
        "city": "São Paulo",
        "state": "SP",
        "zip_code": "01310100"
    }

    response = client.post(
        "/api/delivery-addresses/",
        data=data,
        content_type="application/json",
        **auth_headers
    )

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["address_name"] == "Meu Trabalho"
    assert response_data["city"] == "São Paulo"
    assert DeliveryAddress.objects.filter(user=user).count() == 1


@pytest.mark.django_db
def test_create_delivery_address_invalid_state(client, auth_headers):
    """Testa criação de endereço com estado inválido"""
    data = {
        "address_name": "Casa",
        "address_description": "Rua Teste, 123",
        "city": "São Paulo",
        "state": "XX",
        # Estado inválido
        "zip_code": "01234567"
    }

    response = client.post(
        "/api/delivery-addresses/",
        data=data,
        content_type="application/json",
        **auth_headers
    )

    assert response.status_code == 422


@pytest.mark.django_db
def test_create_delivery_address_missing_fields(client, auth_headers):
    """Testa criação de endereço com campos faltando"""
    data = {
        "address_name": "Casa",
        "city": "São Paulo"
        # Faltam campos obrigatórios
    }

    response = client.post(
        "/api/delivery-addresses/",
        data=data,
        content_type="application/json",
        **auth_headers
    )

    assert response.status_code == 422


@pytest.mark.django_db
def test_create_delivery_address_without_auth(client):
    """Testa criação sem autenticação"""
    data = {
        "address_name": "Casa",
        "address_description": "Rua Teste, 123",
        "city": "São Paulo",
        "state": "SP",
        "zip_code": "01234567"
    }

    response = client.post(
        "/api/delivery-addresses/",
        data=data,
        content_type="application/json"
    )

    assert response.status_code == 401


# --- TESTES PARA UPDATE DELIVERY ADDRESS ---

@pytest.mark.django_db
def test_update_delivery_address_success(client, delivery_address, auth_headers):
    """Testa atualização de endereço com sucesso"""
    data = {
        "address_name": "Casa Atualizada",
        "address_description": "Rua Nova, 999",
        "city": "Campinas",
        "state": "SP",
        "zip_code": "13000000"
    }

    response = client.put(
        f"/api/delivery-addresses/{delivery_address.uuid}",
        data=data,
        content_type="application/json",
        **auth_headers
    )

    assert response.status_code == 200
    delivery_address.refresh_from_db()
    assert delivery_address.address_name == "Casa Atualizada"
    assert delivery_address.city == "Campinas"


@pytest.mark.django_db
def test_update_delivery_address_partial(client, delivery_address, auth_headers):
    """
    Testa atualização parcial de endereço. Mesmo sendo atualização parcial, todos os campos precisam ser passados.
    """
    original_city = delivery_address.city
    data = {
        "address_name": "Nome Atualizado",
        "address_description": delivery_address.address_description,
        "city": delivery_address.city,
        "state": delivery_address.state,
        "zip_code": delivery_address.zip_code
    }

    response = client.put(
        f"/api/delivery-addresses/{delivery_address.uuid}",
        data=data,
        content_type="application/json",
        **auth_headers
    )

    assert response.status_code == 200
    delivery_address.refresh_from_db()
    assert delivery_address.address_name == "Nome Atualizado"
    assert delivery_address.city == original_city  # Não mudou


@pytest.mark.django_db
def test_update_delivery_address_not_found(client, auth_headers):
    """Testa atualização de endereço inexistente"""
    fake_uuid = uuid4()
    data = {
        "address_name": "Casa",
        "address_description": "Rua Teste, 123",
        "city": "São Paulo",
        "state": "SP",
        "zip_code": "01234567"
    }

    response = client.put(
        f"/api/delivery-addresses/{fake_uuid}",
        data=data,
        content_type="application/json",
        **auth_headers
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_update_delivery_address_forbidden_other_user(client, another_delivery_address, auth_headers):
    """Testa que usuário não pode atualizar endereço de outro usuário"""
    data = {
        "address_name": "Tentativa de Atualização",
        "address_description": "Rua Teste, 123",
        "city": "São Paulo",
        "state": "SP",
        "zip_code": "01234567"
    }

    response = client.put(
        f"/api/delivery-addresses/{another_delivery_address.uuid}",
        data=data,
        content_type="application/json",
        **auth_headers
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_update_delivery_address_without_auth(client, delivery_address):
    """Testa atualização sem autenticação"""
    data = {
        "address_name": "Casa",
        "address_description": "Rua Teste, 123",
        "city": "São Paulo",
        "state": "SP",
        "zip_code": "01234567"
    }

    response = client.put(
        f"/api/delivery-addresses/{delivery_address.uuid}",
        data=data,
        content_type="application/json"
    )

    assert response.status_code == 401


# --- TESTES PARA DELETE DELIVERY ADDRESS ---

@pytest.mark.django_db
def test_delete_delivery_address_success(client, delivery_address, auth_headers):
    """Testa exclusão de endereço com sucesso"""
    response = client.delete(f"/api/delivery-addresses/{delivery_address.uuid}", **auth_headers)

    assert response.status_code == 204
    delivery_address.refresh_from_db()
    assert not delivery_address.is_active


@pytest.mark.django_db
def test_delete_delivery_address_not_found(client, auth_headers):
    """Testa exclusão de endereço inexistente"""
    fake_uuid = uuid4()
    response = client.delete(f"/api/delivery-addresses/{fake_uuid}", **auth_headers)
    assert response.status_code == 404


@pytest.mark.django_db
def test_delete_delivery_address_forbidden_other_user(client, another_delivery_address, auth_headers):
    """Testa que usuário não pode excluir endereço de outro usuário"""
    response = client.delete(f"/api/delivery-addresses/{another_delivery_address.uuid}", **auth_headers)
    assert response.status_code == 404


@pytest.mark.django_db
def test_delete_delivery_address_without_auth(client, delivery_address):
    """Testa exclusão sem autenticação"""
    response = client.delete(f"/api/delivery-addresses/{delivery_address.uuid}")
    assert response.status_code == 401