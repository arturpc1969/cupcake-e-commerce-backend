from uuid import uuid4

import pytest
from django.contrib.auth import get_user_model
from django.test import Client

from accounts.utils import create_access_token
from api.models import Order, DeliveryAddress, Product, OrderItem

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
def order(user, delivery_address):
    return Order.objects.create(
        user=user,
        delivery_address=delivery_address,
        payment_method=Order.PaymentMethod.PIX,
        status=Order.OrderStatus.DRAFT
    )


@pytest.fixture
def pending_order(user, delivery_address):
    return Order.objects.create(
        user=user,
        delivery_address=delivery_address,
        payment_method=Order.PaymentMethod.PIX,
        status=Order.OrderStatus.PENDING
    )


@pytest.fixture
def confirmed_order(user, delivery_address):
    return Order.objects.create(
        user=user,
        delivery_address=delivery_address,
        payment_method=Order.PaymentMethod.PIX,
        status=Order.OrderStatus.CONFIRMED
    )


@pytest.fixture
def another_order(another_user, another_delivery_address):
    return Order.objects.create(
        user=another_user,
        delivery_address=another_delivery_address,
        payment_method=Order.PaymentMethod.CREDIT_CARD,
        status=Order.OrderStatus.DRAFT
    )


@pytest.fixture
def product():
    return Product.objects.create(
        name="Produto Teste",
        description="Descrição do produto",
        price=100.00,
        promotion=False
    )


@pytest.fixture
def another_product():
    return Product.objects.create(
        name="Outro Produto",
        description="Outra descrição",
        price=50.00,
        promotion=False
    )


@pytest.fixture
def order_item(order, product):
    return OrderItem.objects.create(
        order=order,
        product=product,
        quantity=2,
        unit_price=product.price
    )


@pytest.fixture
def another_order_item(another_order, product):
    return OrderItem.objects.create(
        order=another_order,
        product=product,
        quantity=1,
        unit_price=product.price
    )


@pytest.fixture
def auth_headers(user):
    token = create_access_token(user.id)
    return {"HTTP_AUTHORIZATION": f"Bearer {token}"}


@pytest.fixture
def staff_auth_headers(staff_user):
    token = create_access_token(staff_user.id)
    return {"HTTP_AUTHORIZATION": f"Bearer {token}"}


# --- TESTES PARA CREATE ORDER ITEM ---

@pytest.mark.django_db
def test_create_order_item_success(client, user, order, product, auth_headers):
    """Testa criação de item no pedido com sucesso"""
    data = {
        "order_uuid": str(order.uuid),
        "product_uuid": str(product.uuid),
        "quantity": 3
    }

    response = client.post(
        "/api/order-items/",
        data=data,
        content_type="application/json",
        **auth_headers
    )

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["order_uuid"] == str(order.uuid)
    assert len(response_data["products"]) == 1
    assert response_data["products"][0]["quantity"] == 3
    assert OrderItem.objects.filter(order=order).count() == 1


@pytest.mark.django_db
def test_create_order_item_in_pending_order(client, user, pending_order, product, auth_headers):
    """Testa criação de item em pedido com status PENDING"""
    data = {
        "order_uuid": str(pending_order.uuid),
        "product_uuid": str(product.uuid),
        "quantity": 2
    }

    response = client.post(
        "/api/order-items/",
        data=data,
        content_type="application/json",
        **auth_headers
    )

    assert response.status_code == 200
    assert OrderItem.objects.filter(order=pending_order).count() == 1


@pytest.mark.django_db
def test_create_order_item_in_confirmed_order(client, user, confirmed_order, product, auth_headers):
    """Testa que não é possível adicionar item em pedido confirmado"""
    data = {
        "order_uuid": str(confirmed_order.uuid),
        "product_uuid": str(product.uuid),
        "quantity": 2
    }

    response = client.post(
        "/api/order-items/",
        data=data,
        content_type="application/json",
        **auth_headers
    )

    assert response.status_code == 400
    assert "cannot add items" in response.json()["detail"].lower()


@pytest.mark.django_db
def test_create_order_item_duplicate_product(client, user, order, product, order_item, auth_headers):
    """Testa que não é possível adicionar o mesmo produto duas vezes"""
    data = {
        "order_uuid": str(order.uuid),
        "product_uuid": str(product.uuid),
        "quantity": 1
    }

    response = client.post(
        "/api/order-items/",
        data=data,
        content_type="application/json",
        **auth_headers
    )

    assert response.status_code == 400
    assert "already exist" in response.json()["detail"].lower()


@pytest.mark.django_db
def test_create_order_item_order_not_found(client, product, auth_headers):
    """Testa criação de item com pedido inexistente"""
    fake_uuid = uuid4()
    data = {
        "order_uuid": str(fake_uuid),
        "product_uuid": str(product.uuid),
        "quantity": 2
    }

    response = client.post(
        "/api/order-items/",
        data=data,
        content_type="application/json",
        **auth_headers
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_create_order_item_product_not_found(client, order, auth_headers):
    """Testa criação de item com produto inexistente"""
    fake_uuid = uuid4()
    data = {
        "order_uuid": str(order.uuid),
        "product_uuid": str(fake_uuid),
        "quantity": 2
    }

    response = client.post(
        "/api/order-items/",
        data=data,
        content_type="application/json",
        **auth_headers
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_create_order_item_forbidden_other_user_order(client, another_order, product, auth_headers):
    """Testa que usuário não pode adicionar item em pedido de outro usuário"""
    data = {
        "order_uuid": str(another_order.uuid),
        "product_uuid": str(product.uuid),
        "quantity": 2
    }

    response = client.post(
        "/api/order-items/",
        data=data,
        content_type="application/json",
        **auth_headers
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_create_order_item_without_auth(client, order, product):
    """Testa criação sem autenticação"""
    data = {
        "order_uuid": str(order.uuid),
        "product_uuid": str(product.uuid),
        "quantity": 2
    }

    response = client.post(
        "/api/order-items/",
        data=data,
        content_type="application/json"
    )

    assert response.status_code == 401


# --- TESTES PARA LIST ORDER ITEMS ---

@pytest.mark.django_db
def test_list_order_items_success(client, user, order, order_item, auth_headers):
    """Testa listagem de pedidos com itens do usuário autenticado"""
    response = client.get("/api/order-items/", **auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["order_uuid"] == str(order.uuid)
    assert len(data[0]["products"]) == 1


@pytest.mark.django_db
def test_list_order_items_only_user_orders(client, user, another_user, order, another_order, order_item,
                                           another_order_item, auth_headers):
    """Testa que usuário só vê seus próprios pedidos com itens"""
    response = client.get("/api/order-items/", **auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["order_uuid"] == str(order.uuid)


@pytest.mark.django_db
def test_list_order_items_empty(client, auth_headers):
    """Testa listagem quando não há pedidos"""
    response = client.get("/api/order-items/", **auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0


@pytest.mark.django_db
def test_list_order_items_without_auth(client):
    """Testa listagem sem autenticação"""
    response = client.get("/api/order-items/")
    assert response.status_code == 401


# --- TESTES PARA LIST ORDER ITEMS STAFF ---

@pytest.mark.django_db
def test_list_order_items_staff_success(client, order, another_order, order_item, another_order_item,
                                        staff_auth_headers):
    """Testa listagem de todos os pedidos com itens para staff"""
    response = client.get("/api/order-items/admin", **staff_auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    uuids = [item["order_uuid"] for item in data]
    assert str(order.uuid) in uuids
    assert str(another_order.uuid) in uuids


@pytest.mark.django_db
def test_list_order_items_staff_forbidden_for_regular_user(client, auth_headers):
    """Testa que usuário comum não pode acessar rota de staff"""
    response = client.get("/api/order-items/admin", **auth_headers)
    assert response.status_code == 403


# --- TESTES PARA GET ORDER ITEM ---

@pytest.mark.django_db
def test_get_order_item_success(client, user, order, order_item, auth_headers):
    """Testa busca de pedido com itens específico"""
    response = client.get(f"/api/order-items/{order.uuid}", **auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["order_uuid"] == str(order.uuid)
    assert len(data["products"]) == 1
    assert data["products"][0]["quantity"] == order_item.quantity


@pytest.mark.django_db
def test_get_order_item_not_found(client, auth_headers):
    """Testa busca de pedido inexistente"""
    fake_uuid = uuid4()
    response = client.get(f"/api/order-items/{fake_uuid}", **auth_headers)
    assert response.status_code == 404


@pytest.mark.django_db
def test_get_order_item_forbidden_other_user(client, another_order, auth_headers):
    """Testa que usuário não pode ver pedido de outro usuário"""
    response = client.get(f"/api/order-items/{another_order.uuid}", **auth_headers)
    assert response.status_code == 404


@pytest.mark.django_db
def test_get_order_item_without_auth(client, order):
    """Testa busca sem autenticação"""
    response = client.get(f"/api/order-items/{order.uuid}")
    assert response.status_code == 401


# --- TESTES PARA GET ORDER ITEM STAFF ---

@pytest.mark.django_db
def test_get_order_item_staff_success(client, order, order_item, staff_auth_headers):
    """Testa busca de pedido com itens específico para staff"""
    response = client.get(f"/api/order-items/admin/{order.uuid}", **staff_auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["order_uuid"] == str(order.uuid)
    assert "user" in data  # Staff vê informações do usuário


@pytest.mark.django_db
def test_get_order_item_staff_forbidden_for_regular_user(client, order, auth_headers):
    """Testa que usuário comum não pode acessar rota de staff"""
    response = client.get(f"/api/order-items/admin/{order.uuid}", **auth_headers)
    assert response.status_code == 403


@pytest.mark.django_db
def test_get_order_item_staff_not_found(client, staff_auth_headers):
    """Testa busca de pedido inexistente para staff"""
    fake_uuid = uuid4()
    response = client.get(f"/api/order-items/admin/{fake_uuid}", **staff_auth_headers)
    assert response.status_code == 404


# --- TESTES PARA UPDATE ORDER ITEM ---

@pytest.mark.django_db
def test_update_order_item_success(client, order, product, order_item, auth_headers):
    """Testa atualização de item do pedido com sucesso"""
    data = {
        "order_uuid": str(order.uuid),
        "product_uuid": str(product.uuid),
        "quantity": 5
    }

    response = client.put(
        "/api/order-items/",
        data=data,
        content_type="application/json",
        **auth_headers
    )

    assert response.status_code == 200
    order_item.refresh_from_db()
    assert order_item.quantity == 5


@pytest.mark.django_db
def test_update_order_item_not_found(client, order, auth_headers):
    """Testa atualização de item inexistente"""
    fake_product_uuid = uuid4()
    data = {
        "order_uuid": str(order.uuid),
        "product_uuid": str(fake_product_uuid),
        "quantity": 5
    }

    response = client.put(
        "/api/order-items/",
        data=data,
        content_type="application/json",
        **auth_headers
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_update_order_item_forbidden_other_user(client, another_order, product, another_order_item, auth_headers):
    """Testa que usuário não pode atualizar item de pedido de outro usuário"""
    data = {
        "order_uuid": str(another_order.uuid),
        "product_uuid": str(product.uuid),
        "quantity": 5
    }

    response = client.put(
        "/api/order-items/",
        data=data,
        content_type="application/json",
        **auth_headers
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_update_order_item_without_auth(client, order, product):
    """Testa atualização sem autenticação"""
    data = {
        "order_uuid": str(order.uuid),
        "product_uuid": str(product.uuid),
        "quantity": 5
    }

    response = client.put(
        "/api/order-items/",
        data=data,
        content_type="application/json"
    )

    assert response.status_code == 401


# --- TESTES PARA DELETE ORDER ITEM ---

@pytest.mark.django_db
def test_delete_order_item_success(client, order, product, order_item, auth_headers):
    """Testa exclusão de item do pedido com sucesso"""
    response = client.delete(
        f"/api/order-items/{order.uuid}/{product.uuid}",
        **auth_headers
    )

    assert response.status_code == 204
    assert OrderItem.objects.filter(order=order, product=product).count() == 0


@pytest.mark.django_db
def test_delete_order_item_in_confirmed_order(client, confirmed_order, product, auth_headers):
    """Testa que não é possível excluir item de pedido confirmado"""
    order_item = OrderItem.objects.create(
        order=confirmed_order,
        product=product,
        quantity=1,
        unit_price=product.price
    )

    response = client.delete(
        f"/api/order-items/{confirmed_order.uuid}/{product.uuid}",
        **auth_headers
    )

    assert response.status_code == 400
    assert "cannot delete items" in response.json()["detail"].lower()


@pytest.mark.django_db
def test_delete_order_item_not_found(client, order, auth_headers):
    """Testa exclusão de item inexistente"""
    fake_product_uuid = uuid4()
    response = client.delete(
        f"/api/order-items/{order.uuid}/{fake_product_uuid}",
        **auth_headers
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_delete_order_item_forbidden_other_user(client, another_order, product, another_order_item, auth_headers):
    """Testa que usuário não pode excluir item de pedido de outro usuário"""
    response = client.delete(
        f"/api/order-items/{another_order.uuid}/{product.uuid}",
        **auth_headers
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_delete_order_item_without_auth(client, order, product):
    """Testa exclusão sem autenticação"""
    response = client.delete(f"/api/order-items/{order.uuid}/{product.uuid}")
    assert response.status_code == 401


# --- TESTES PARA DELETE ORDER ITEM STAFF ---

@pytest.mark.django_db
def test_delete_order_item_staff_success(client, order, product, order_item, staff_auth_headers):
    """Testa exclusão de item do pedido por staff"""
    response = client.delete(
        f"/api/order-items/admin/{order.uuid}/{product.uuid}",
        **staff_auth_headers
    )

    assert response.status_code == 204
    assert OrderItem.objects.filter(order=order, product=product).count() == 0


@pytest.mark.django_db
def test_delete_order_item_staff_forbidden_for_regular_user(client, order, product, order_item, auth_headers):
    """Testa que usuário comum não pode usar rota de staff para exclusão"""
    response = client.delete(
        f"/api/order-items/admin/{order.uuid}/{product.uuid}",
        **auth_headers
    )

    assert response.status_code == 403


@pytest.mark.django_db
def test_delete_order_item_staff_not_found(client, order, staff_auth_headers):
    """Testa exclusão de item inexistente por staff"""
    fake_product_uuid = uuid4()
    response = client.delete(
        f"/api/order-items/admin/{order.uuid}/{fake_product_uuid}",
        **staff_auth_headers
    )

    assert response.status_code == 404
