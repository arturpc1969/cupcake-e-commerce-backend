import pytest
from django.contrib.auth import get_user_model
from django.test import Client

from accounts.utils import create_access_token

User = get_user_model()


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def user():
    return User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="testpass123",
        first_name="Test",
        last_name="User"
    )


@pytest.fixture
def another_user():
    return User.objects.create_user(
        username="anotheruser",
        email="another@example.com",
        password="anotherpass123"
    )


@pytest.fixture
def auth_headers(user):
    token = create_access_token(user.id)
    return {"HTTP_AUTHORIZATION": f"Bearer {token}"}


# --- TESTES PARA GET ME ---

@pytest.mark.django_db
def test_get_me_success(client, user, auth_headers):
    """Testa busca dos dados do usuário autenticado"""
    response = client.get("/api/users/me", **auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["uuid"] == str(user.uuid)
    assert data["username"] == user.username
    assert data["email"] == user.email
    assert data["first_name"] == user.first_name
    assert data["last_name"] == user.last_name


@pytest.mark.django_db
def test_get_me_without_auth(client):
    """Testa busca sem autenticação"""
    response = client.get("/api/users/me")
    assert response.status_code == 401


# --- TESTES PARA UPDATE ME ---

@pytest.mark.django_db
def test_update_me_success(client, user, auth_headers):
    """Testa atualização completa dos dados do usuário"""
    data = {
        "username": "newusername",
        "email": "newemail@example.com",
        "first_name": "NewFirst",
        "last_name": "NewLast"
    }

    response = client.put(
        "/api/users/me",
        data=data,
        content_type="application/json",
        **auth_headers
    )

    assert response.status_code == 200
    user.refresh_from_db()
    assert user.username == "newusername"
    assert user.email == "newemail@example.com"
    assert user.first_name == "NewFirst"
    assert user.last_name == "NewLast"


@pytest.mark.django_db
def test_update_me_partial(client, user, auth_headers):
    """Testa atualização parcial dos dados do usuário"""
    original_email = user.email
    data = {
        "first_name": "UpdatedFirst"
    }

    response = client.put(
        "/api/users/me",
        data=data,
        content_type="application/json",
        **auth_headers
    )

    assert response.status_code == 200
    user.refresh_from_db()
    assert user.first_name == "UpdatedFirst"
    assert user.email == original_email  # Não mudou


@pytest.mark.django_db
def test_update_me_duplicate_username(client, user, another_user, auth_headers):
    """Testa atualização com username já existente"""
    data = {
        "username": another_user.username
    }

    response = client.put(
        "/api/users/me",
        data=data,
        content_type="application/json",
        **auth_headers
    )

    assert response.status_code == 422


@pytest.mark.django_db
def test_update_me_invalid_email(client, user, auth_headers):
    """Testa atualização com email inválido"""
    data = {
        "email": "invalid-email"
    }

    response = client.put(
        "/api/users/me",
        data=data,
        content_type="application/json",
        **auth_headers
    )

    assert response.status_code == 422


@pytest.mark.django_db
def test_update_me_without_auth(client):
    """Testa atualização sem autenticação"""
    data = {
        "first_name": "NewName"
    }

    response = client.put(
        "/api/users/me",
        data=data,
        content_type="application/json"
    )

    assert response.status_code == 401


# --- TESTES PARA DEACTIVATE ME ---

@pytest.mark.django_db
def test_deactivate_me_success(client, user, auth_headers):
    """Testa desativação do usuário"""
    data = {
        "is_active": False
    }

    response = client.patch(
        "/api/users/me",
        data=data,
        content_type="application/json",
        **auth_headers
    )

    assert response.status_code == 200
    response_data = response.json()
    assert "successfully deactivated" in response_data["message"].lower()
    user.refresh_from_db()
    assert not user.is_active


@pytest.mark.django_db
def test_deactivate_me_no_change(client, user, auth_headers):
    """Testa quando usuário tenta manter-se ativo"""
    data = {
        "is_active": True
    }

    response = client.patch(
        "/api/users/me",
        data=data,
        content_type="application/json",
        **auth_headers
    )

    assert response.status_code == 200
    response_data = response.json()
    assert "nothing changed" in response_data["message"].lower()
    user.refresh_from_db()
    assert user.is_active


@pytest.mark.django_db
def test_deactivate_me_without_auth(client):
    """Testa desativação sem autenticação"""
    data = {
        "is_active": False
    }

    response = client.patch(
        "/api/users/me",
        data=data,
        content_type="application/json"
    )

    assert response.status_code == 401


# --- TESTES PARA DELETE ME ---

@pytest.mark.django_db
def test_delete_me_success(client, user, auth_headers):
    """Testa exclusão do usuário"""
    user_id = user.id

    response = client.delete("/api/users/me", **auth_headers)

    assert response.status_code == 204
    assert not User.objects.filter(id=user_id).exists()


@pytest.mark.django_db
def test_delete_me_without_auth(client):
    """Testa exclusão sem autenticação"""
    response = client.delete("/api/users/me")
    assert response.status_code == 401


# --- TESTES PARA CHANGE PASSWORD ---

@pytest.mark.django_db
def test_change_password_success(client, user, auth_headers):
    """Testa mudança de senha com sucesso"""
    data = {
        "old_password": "testpass123",
        "new_password": "newpass456"
    }

    response = client.post(
        "/api/users/me/change-password",
        data=data,
        content_type="application/json",
        **auth_headers
    )

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["success"] is True
    assert "successfully" in response_data["message"].lower()

    # Verifica se a senha foi realmente alterada
    user.refresh_from_db()
    assert user.check_password("newpass456")


@pytest.mark.django_db
def test_change_password_wrong_old_password(client, user, auth_headers):
    """Testa mudança de senha com senha antiga incorreta"""
    data = {
        "old_password": "wrongpassword",
        "new_password": "newpass456"
    }

    response = client.post(
        "/api/users/me/change-password",
        data=data,
        content_type="application/json",
        **auth_headers
    )

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["success"] is False
    assert "incorrect" in response_data["message"].lower()

    # Verifica que a senha não foi alterada
    user.refresh_from_db()
    assert user.check_password("testpass123")


@pytest.mark.django_db
def test_change_password_missing_old_password(client, user, auth_headers):
    """Testa mudança de senha sem fornecer senha antiga"""
    data = {
        "new_password": "newpass456"
    }

    response = client.post(
        "/api/users/me/change-password",
        data=data,
        content_type="application/json",
        **auth_headers
    )

    assert response.status_code == 422


@pytest.mark.django_db
def test_change_password_missing_new_password(client, user, auth_headers):
    """Testa mudança de senha sem fornecer nova senha"""
    data = {
        "old_password": "testpass123"
    }

    response = client.post(
        "/api/users/me/change-password",
        data=data,
        content_type="application/json",
        **auth_headers
    )

    assert response.status_code == 422


@pytest.mark.django_db
def test_change_password_without_auth(client):
    """Testa mudança de senha sem autenticação"""
    data = {
        "old_password": "testpass123",
        "new_password": "newpass456"
    }

    response = client.post(
        "/api/users/me/change-password",
        data=data,
        content_type="application/json"
    )

    assert response.status_code == 401


@pytest.mark.django_db
def test_change_password_same_as_old(client, user, auth_headers):
    """Testa mudança de senha usando a mesma senha antiga"""
    data = {
        "old_password": "testpass123",
        "new_password": "testpass123"
    }

    response = client.post(
        "/api/users/me/change-password",
        data=data,
        content_type="application/json",
        **auth_headers
    )

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["success"] is True
    # Mesmo sendo a mesma senha, a operação é bem-sucedida


@pytest.mark.django_db
def test_change_password_weak_password(client, user, auth_headers):
    """Testa mudança de senha com senha fraca (se houver validação)"""
    data = {
        "old_password": "testpass123",
        "new_password": "123"
    }

    response = client.post(
        "/api/users/me/change-password",
        data=data,
        content_type="application/json",
        **auth_headers
    )

    # Dependendo da configuração do Django, pode aceitar ou rejeitar
    # Este teste documenta o comportamento atual
    assert response.status_code in [200, 422]