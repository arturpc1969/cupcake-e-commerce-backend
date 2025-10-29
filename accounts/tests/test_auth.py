import pytest
from django.contrib.auth import get_user_model
from django.test import Client

from accounts.utils import create_refresh_token, decode_token

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
        last_name="User",
        cpf="12345678901"
    )


# --- TESTES PARA SIGNUP ---

@pytest.mark.django_db
def test_signup_success(client):
    """Testa criação de usuário com sucesso"""
    data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "newpass123",
        "first_name": "New",
        "last_name": "User",
        "cpf": "98765432100"
    }

    response = client.post(
        "/api/auth/signup",
        data=data,
        content_type="application/json"
    )

    assert response.status_code == 200
    response_data = response.json()
    assert "message" in response_data
    assert "successfully created" in response_data["message"].lower()
    assert "uuid" in response_data

    # Verifica se o usuário foi realmente criado
    assert User.objects.filter(username="newuser").exists()
    created_user = User.objects.get(username="newuser")
    assert created_user.email == "newuser@example.com"
    assert created_user.first_name == "New"
    assert created_user.last_name == "User"
    assert created_user.cpf == "98765432100"


@pytest.mark.django_db
def test_signup_duplicate_username(client, user):
    """Testa criação de usuário com username já existente"""
    data = {
        "username": user.username,
        "email": "different@example.com",
        "password": "newpass123",
        "first_name": "Different",
        "last_name": "User",
        "cpf": "98765432100"
    }

    response = client.post(
        "/api/auth/signup",
        data=data,
        content_type="application/json"
    )

    assert response.status_code == 200
    response_data = response.json()
    assert "error" in response_data
    assert "already exists" in response_data["error"].lower()


@pytest.mark.django_db
def test_signup_missing_required_fields(client):
    """Testa criação de usuário sem campos obrigatórios"""
    data = {
        "username": "incomplete"
    }

    response = client.post(
        "/api/auth/signup",
        data=data,
        content_type="application/json"
    )

    assert response.status_code == 422


@pytest.mark.django_db
def test_signup_invalid_email(client):
    """Testa criação de usuário com email inválido"""
    data = {
        "username": "newuser",
        "email": "invalid-email",
        "password": "newpass123",
        "first_name": "New",
        "last_name": "User",
        "cpf": "98765432100"
    }

    response = client.post(
        "/api/auth/signup",
        data=data,
        content_type="application/json"
    )

    assert response.status_code == 422


# --- TESTES PARA LOGIN ---

@pytest.mark.django_db
def test_login_success(client, user):
    """Testa login com credenciais válidas"""
    data = {
        "username": "testuser",
        "password": "testpass123"
    }

    response = client.post(
        "/api/auth/login",
        data=data,
        content_type="application/json"
    )

    assert response.status_code == 200
    response_data = response.json()
    assert "access" in response_data
    assert "refresh" in response_data

    # Verifica se os tokens são válidos
    access_payload = decode_token(response_data["access"])
    refresh_payload = decode_token(response_data["refresh"])
    assert access_payload is not None
    assert refresh_payload is not None
    assert access_payload["user_id"] == user.id
    assert refresh_payload["user_id"] == user.id
    assert access_payload["type"] == "access"
    assert refresh_payload["type"] == "refresh"


@pytest.mark.django_db
def test_login_invalid_username(client, user):
    """Testa login com username inválido"""
    data = {
        "username": "wronguser",
        "password": "testpass123"
    }

    response = client.post(
        "/api/auth/login",
        data=data,
        content_type="application/json"
    )

    assert response.status_code == 401
    response_data = response.json()
    assert "error" in response_data
    assert "invalid credentials" in response_data["error"].lower()


@pytest.mark.django_db
def test_login_invalid_password(client, user):
    """Testa login com senha inválida"""
    data = {
        "username": "testuser",
        "password": "wrongpassword"
    }

    response = client.post(
        "/api/auth/login",
        data=data,
        content_type="application/json"
    )

    assert response.status_code == 401
    response_data = response.json()
    assert "error" in response_data
    assert "invalid credentials" in response_data["error"].lower()


@pytest.mark.django_db
def test_login_missing_username(client):
    """Testa login sem username"""
    data = {
        "password": "testpass123"
    }

    response = client.post(
        "/api/auth/login",
        data=data,
        content_type="application/json"
    )

    assert response.status_code == 422


@pytest.mark.django_db
def test_login_missing_password(client):
    """Testa login sem senha"""
    data = {
        "username": "testuser"
    }

    response = client.post(
        "/api/auth/login",
        data=data,
        content_type="application/json"
    )

    assert response.status_code == 422


@pytest.mark.django_db
def test_login_inactive_user(client, user):
    """Testa login com usuário inativo"""
    user.is_active = False
    user.save()

    data = {
        "username": "testuser",
        "password": "testpass123"
    }

    response = client.post(
        "/api/auth/login",
        data=data,
        content_type="application/json"
    )

    assert response.status_code == 401
    response_data = response.json()
    assert "error" in response_data


# --- TESTES PARA REFRESH TOKEN ---

@pytest.mark.django_db
def test_refresh_token_success(client, user):
    """Testa renovação de token com refresh token válido"""
    refresh_token = create_refresh_token(user.id)

    data = {
        "refresh": refresh_token
    }

    response = client.post(
        "/api/auth/refresh",
        data=data,
        content_type="application/json"
    )

    assert response.status_code == 200
    response_data = response.json()
    assert "access" in response_data
    assert "refresh" in response_data

    # Verifica se os novos tokens são válidos
    access_payload = decode_token(response_data["access"])
    refresh_payload = decode_token(response_data["refresh"])
    assert access_payload is not None
    assert refresh_payload is not None
    assert access_payload["user_id"] == user.id
    assert refresh_payload["user_id"] == user.id


@pytest.mark.django_db
def test_refresh_token_invalid_token(client):
    """Testa renovação com token inválido"""
    data = {
        "refresh": "invalid.token.here"
    }

    response = client.post(
        "/api/auth/refresh",
        data=data,
        content_type="application/json"
    )

    assert response.status_code == 401
    response_data = response.json()
    assert "error" in response_data
    assert "invalid" in response_data["error"].lower()


@pytest.mark.django_db
def test_refresh_token_with_access_token(client, user):
    """Testa renovação usando access token ao invés de refresh token"""
    from accounts.utils import create_access_token
    access_token = create_access_token(user.id)

    data = {
        "refresh": access_token
    }

    response = client.post(
        "/api/auth/refresh",
        data=data,
        content_type="application/json"
    )

    assert response.status_code == 401
    response_data = response.json()
    assert "error" in response_data
    assert "invalid" in response_data["error"].lower()


@pytest.mark.django_db
def test_refresh_token_missing_token(client):
    """Testa renovação sem fornecer token"""
    data = {}

    response = client.post(
        "/api/auth/refresh",
        data=data,
        content_type="application/json"
    )

    assert response.status_code == 422


@pytest.mark.django_db
def test_refresh_token_expired(client, user):
    """Testa renovação com token expirado"""
    # Este teste documenta o comportamento com token expirado
    # A implementação real depende de como decode_token trata tokens expirados
    import jwt
    from accounts.utils import SECRET_KEY, ALGORITHM
    from datetime import datetime, timedelta

    expired_payload = {
        "user_id": user.id,
        "type": "refresh",
        "exp": datetime.utcnow() - timedelta(days=1)
    }
    expired_token = jwt.encode(expired_payload, SECRET_KEY, algorithm=ALGORITHM)

    data = {
        "refresh": expired_token
    }

    response = client.post(
        "/api/auth/refresh",
        data=data,
        content_type="application/json"
    )

    assert response.status_code == 401
    response_data = response.json()
    assert "error" in response_data


@pytest.mark.django_db
def test_refresh_token_nonexistent_user(client):
    """Testa renovação com token de usuário inexistente"""
    refresh_token = create_refresh_token(
        99999)  # ID que não existe

    data = {
        "refresh": refresh_token
    }

    response = client.post(
        "/api/auth/refresh",
        data=data,
        content_type="application/json"
    )

    # O endpoint atual não valida se o usuário existe, apenas decodifica o token
    # Este teste documenta o comportamento atual
    assert response.status_code == 200
    response_data = response.json()
    assert "access" in response_data
    assert "refresh" in response_data
