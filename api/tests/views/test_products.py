from io import BytesIO
from uuid import uuid4

import pytest
from PIL import Image
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client
from rest_framework.test import APIClient

from accounts.utils import create_access_token
from api.models import Product

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
def product():
    return Product.objects.create(
        name="Cupcake de Chocolate",
        description="Delicioso cupcake de chocolate com cobertura",
        price=15.50,
        image=None
    )


@pytest.fixture
def another_product():
    return Product.objects.create(
        name="Cupcake de Morango",
        description="Cupcake de morango com chantilly",
        price=12.00
    )


@pytest.fixture
def auth_headers(user):
    token = create_access_token(user.id)
    return {"HTTP_AUTHORIZATION": f"Bearer {token}"}


@pytest.fixture
def staff_auth_headers(staff_user):
    token = create_access_token(staff_user.id)
    return {"HTTP_AUTHORIZATION": f"Bearer {token}"}


@pytest.fixture
def sample_image():
    """Cria uma imagem de teste"""
    image = Image.new('RGB', (100, 100), color='red')
    image_io = BytesIO()
    image.save(image_io, format='JPEG')
    image_io.seek(0)
    return SimpleUploadedFile(
        "test_image.jpg",
        image_io.getvalue(),
        content_type="image/jpeg"
    )


# --- TESTES PARA LIST PRODUCTS ---

@pytest.mark.django_db
def test_list_products_success(client, product, another_product):
    """Testa listagem de produtos (endpoint público)"""
    response = client.get("/api/products/")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    names = [item["name"] for item in data]
    assert product.name in names
    assert another_product.name in names


@pytest.mark.django_db
def test_list_products_empty(client):
    """Testa listagem quando não há produtos"""
    response = client.get("/api/products/")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0


# --- TESTES PARA GET PRODUCT ---

@pytest.mark.django_db
def test_get_product_success(client, product):
    """Testa busca de produto específico (endpoint público)"""
    response = client.get(f"/api/products/{product.uuid}")

    assert response.status_code == 200
    data = response.json()
    assert data["uuid"] == str(product.uuid)
    assert data["name"] == product.name
    assert data["price"] == product.price


@pytest.mark.django_db
def test_get_product_not_found(client):
    """Testa busca de produto inexistente"""
    fake_uuid = uuid4()
    response = client.get(f"/api/products/{fake_uuid}")
    assert response.status_code == 404


# --- TESTES PARA CREATE PRODUCT ---

@pytest.mark.django_db
def test_create_product_success(client, staff_auth_headers):
    """Testa criação de produto com sucesso (staff)"""
    data = {
        "name": "Cupcake de Baunilha",
        "description": "Cupcake de baunilha com glacê",
        "price": 13.50,
        "promotion": False
    }

    response = client.post(
        "/api/products/",
        data=data,
        **staff_auth_headers
    )

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["name"] == "Cupcake de Baunilha"
    assert response_data["price"] == 13.50
    assert Product.objects.filter(name="Cupcake de Baunilha").exists()


@pytest.mark.django_db
def test_create_product_with_image(staff_auth_headers, sample_image, mocker):
    """Testa criação de produto com imagem"""
    # Mock do upload do Cloudinary
    mock_upload = mocker.patch('cloudinary.uploader.upload')
    mock_upload.return_value = {
        'public_id': 'test_image_id',
        'url': 'https://res.cloudinary.com/test/image/upload/test_image.jpg',
        'secure_url': 'https://res.cloudinary.com/test/image/upload/test_image.jpg'
    }

    # Mock do CloudinaryResource para evitar erro ao gerar URL
    mock_cloudinary_resource = mocker.patch('cloudinary.CloudinaryResource.build_url')
    mock_cloudinary_resource.return_value = 'https://res.cloudinary.com/test/image/upload/test_image.jpg'

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=staff_auth_headers["HTTP_AUTHORIZATION"])

    data = {
        "name": "Cupcake com Imagem",
        "description": "Cupcake com foto",
        "price": 16.00,
        "promotion": False,
        "image": sample_image
    }

    response = client.post(
        "/api/products/",
        data=data,
        format="multipart"
    )

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["name"] == "Cupcake com Imagem"
    assert response_data["image"] is not None
    assert Product.objects.filter(name="Cupcake com Imagem").exists()

    # Verifica que o upload foi chamado
    mock_upload.assert_called_once()


@pytest.mark.django_db
def test_create_product_forbidden_for_regular_user(client, auth_headers):
    """Testa que usuário comum não pode criar produto"""
    data = {
        "name": "Cupcake Proibido",
        "description": "Este não deveria ser criado",
        "price": 10.00,
        "promotion": False
    }

    response = client.post(
        "/api/products/",
        data=data,
        **auth_headers
    )

    assert response.status_code == 403


@pytest.mark.django_db
def test_create_product_without_auth(client):
    """Testa criação sem autenticação"""
    data = {
        "name": "Cupcake Sem Auth",
        "description": "Sem autenticação",
        "price": 10.00
    }

    response = client.post("/api/products/", data=data)
    assert response.status_code == 401


@pytest.mark.django_db
def test_create_product_invalid_data(client, staff_auth_headers):
    """Testa criação com dados inválidos"""
    data = {
        "name": "",
        # Nome vazio
        "description": "Descrição válida",
        "price": -5.00
        # Preço negativo
    }

    response = client.post(
        "/api/products/",
        data=data,
        **staff_auth_headers
    )

    assert response.status_code == 422


# --- TESTES PARA UPDATE PRODUCT ---

@pytest.mark.django_db
def test_update_product_success(product, staff_auth_headers, tmp_path, mocker):
    """
    Testa atualização de produto com sucesso.
    Usa APIClient do rest_framework.test porque o client do Django tem problemas no teste com PUT e multipart/form-data.
    """
    # Mock do upload do Cloudinary
    mock_upload = mocker.patch('cloudinary.uploader.upload')
    mock_upload.return_value = {
        'public_id': 'test_image_id',
        'url': 'https://res.cloudinary.com/test/image/upload/test_image.jpg',
        'secure_url': 'https://res.cloudinary.com/test/image/upload/test_image.jpg'
    }

    # Mock do CloudinaryResource para evitar erro ao gerar URL
    mock_cloudinary_resource = mocker.patch('cloudinary.CloudinaryResource.build_url')
    mock_cloudinary_resource.return_value = 'https://res.cloudinary.com/test/image/upload/test_image.jpg'

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=staff_auth_headers["HTTP_AUTHORIZATION"])

    # Cria um arquivo temporário simulando o upload de imagem
    image_path = tmp_path / "cupcake_2.webp"
    image_path.write_bytes(b"fake image content")

    with open(image_path, "rb") as image_file:
        data = {
            "name": "Cupcake Atualizado",
            "description": "Descrição atualizada",
            "price": 18.00,
            "promotion": False,
            "image": image_file,
        }

        response = client.put(
            f"/api/products/{product.uuid}",
            data,
            format="multipart"
        )

    assert response.status_code == 200
    product.refresh_from_db()
    assert product.name == "Cupcake Atualizado"
    assert product.price == 18.00

    # Verifica que o upload foi chamado
    mock_upload.assert_called_once()


@pytest.mark.django_db
def test_update_product_with_image(product, staff_auth_headers, tmp_path, mocker):
    """
    Testa atualização de produto com nova imagem.
    Usa APIClient do rest_framework.test porque o client do Django tem problemas no teste com PUT e multipart/form-data.
    """
    # Mock do upload do Cloudinary
    mock_upload = mocker.patch('cloudinary.uploader.upload')
    mock_upload.return_value = {
        'public_id': 'test_image_id',
        'url': 'https://res.cloudinary.com/test/image/upload/test_image.jpg',
        'secure_url': 'https://res.cloudinary.com/test/image/upload/test_image.jpg'
    }

    # Mock do CloudinaryResource para evitar erro ao gerar URL
    mock_cloudinary_resource = mocker.patch('cloudinary.CloudinaryResource.build_url')
    mock_cloudinary_resource.return_value = 'https://res.cloudinary.com/test/image/upload/test_image.jpg'

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=staff_auth_headers["HTTP_AUTHORIZATION"])

    # Cria um arquivo temporário simulando o upload de imagem
    image_path = tmp_path / "cupcake_2.webp"
    image_path.write_bytes(b"fake image content")

    with open(image_path, "rb") as image_file:
        data = {
            "name": "Cupcake com Nova Imagem",
            "description": "Descrição com imagem",
            "price": 20.00,
            "promotion": False,
            "image": image_file
        }

        response = client.put(
            f"/api/products/{product.uuid}",
            data,
            format="multipart"
        )

    assert response.status_code == 200
    product.refresh_from_db()
    assert product.name == "Cupcake com Nova Imagem"
    assert product.image is not None

    # Verifica que o upload foi chamado
    mock_upload.assert_called_once()


@pytest.mark.django_db
def test_update_product_forbidden_for_regular_user(product, auth_headers, tmp_path):
    """
    Testa que usuário comum não pode atualizar produto.
    Usa APIClient do rest_framework.test porque o client do Django tem problemas no teste com PUT e multipart/form-data.
    """
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=auth_headers["HTTP_AUTHORIZATION"])

    # Cria um arquivo temporário simulando o upload de imagem
    image_path = tmp_path / "cupcake_2.webp"
    image_path.write_bytes(b"fake image content")

    with open(image_path, "rb") as image_file:
        data = {
            "name": "Tentativa de Atualização",
            "description": "Não deveria funcionar",
            "price": 15.00,
            "promotion": False,
            "image": image_file
        }

        response = client.put(
            f"/api/products/{product.uuid}",
            data,
            format="multipart"
        )

    assert response.status_code == 403


@pytest.mark.django_db
def test_update_product_not_found(staff_auth_headers, tmp_path):
    """
    Testa atualização de produto inexistente.
    Usa APIClient do rest_framework.test porque o client do Django tem problemas no teste com PUT e multipart/form-data.
    """
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=staff_auth_headers["HTTP_AUTHORIZATION"])

    fake_uuid = uuid4()

    # Cria um arquivo temporário simulando o upload de imagem
    image_path = tmp_path / "cupcake_2.webp"
    image_path.write_bytes(b"fake image content")

    with open(image_path, "rb") as image_file:
        data = {
            "name": "Produto Inexistente",
            "description": "Não existe",
            "price": 10.00,
            "promotion": False,
            "image": image_file,
        }

        response = client.put(
            f"/api/products/{fake_uuid}",
            data,
            format="multipart"
        )

    assert response.status_code == 404


# --- TESTES PARA DELETE PRODUCT ---

@pytest.mark.django_db
def test_delete_product_success(client, product, staff_auth_headers):
    """Testa exclusão de produto com sucesso (soft delete)"""
    response = client.delete(f"/api/products/{product.uuid}", **staff_auth_headers)

    assert response.status_code == 204
    product.refresh_from_db()
    assert not product.is_active


@pytest.mark.django_db
def test_delete_product_forbidden_for_regular_user(client, product, auth_headers):
    """Testa que usuário comum não pode excluir produto"""
    response = client.delete(f"/api/products/{product.uuid}", **auth_headers)
    assert response.status_code == 403


@pytest.mark.django_db
def test_delete_product_without_auth(client, product):
    """Testa exclusão sem autenticação"""
    response = client.delete(f"/api/products/{product.uuid}")
    assert response.status_code == 401


@pytest.mark.django_db
def test_delete_product_not_found(client, staff_auth_headers):
    """Testa exclusão de produto inexistente"""
    fake_uuid = uuid4()
    response = client.delete(f"/api/products/{fake_uuid}", **staff_auth_headers)
    assert response.status_code == 404


# --- TESTES PARA UPLOAD IMAGE ---

@pytest.mark.django_db
def test_upload_product_image_success(client, product, staff_auth_headers, sample_image, mocker):
    """Testa upload de imagem para produto existente"""
    # Mock do upload do Cloudinary
    mock_upload = mocker.patch('cloudinary.uploader.upload')
    mock_upload.return_value = {
        'public_id': 'test_image_id',
        'url': 'https://res.cloudinary.com/test/image/upload/test_image.jpg',
        'secure_url': 'https://res.cloudinary.com/test/image/upload/test_image.jpg'
    }

    # Mock do CloudinaryResource para evitar erro ao gerar URL
    mock_cloudinary_resource = mocker.patch('cloudinary.CloudinaryResource.build_url')
    mock_cloudinary_resource.return_value = 'https://res.cloudinary.com/test/image/upload/test_image.jpg'

    response = client.post(
        f"/api/products/{product.uuid}/upload-image",
        data={"image": sample_image},
        **staff_auth_headers
    )

    assert response.status_code == 200
    product.refresh_from_db()
    assert product.image is not None

    # Verifica que o upload foi chamado
    mock_upload.assert_called_once()


@pytest.mark.django_db
def test_upload_product_image_forbidden_for_regular_user(client, product, auth_headers, sample_image):
    """Testa que usuário comum não pode fazer upload de imagem"""
    response = client.post(
        f"/api/products/{product.uuid}/upload-image",
        data={"image": sample_image},
        **auth_headers
    )

    assert response.status_code == 403


@pytest.mark.django_db
def test_upload_product_image_without_auth(client, product, sample_image):
    """Testa upload sem autenticação"""
    response = client.post(
        f"/api/products/{product.uuid}/upload-image",
        data={"image": sample_image}
    )
    assert response.status_code == 401


@pytest.mark.django_db
def test_upload_product_image_not_found(client, staff_auth_headers, sample_image):
    """Testa upload para produto inexistente"""
    fake_uuid = uuid4()
    response = client.post(
        f"/api/products/{fake_uuid}/upload-image",
        data={"image": sample_image},
        **staff_auth_headers
    )
    assert response.status_code == 404


@pytest.mark.django_db
def test_upload_product_image_missing_file(client, product, staff_auth_headers):
    """Testa upload sem arquivo de imagem"""
    response = client.post(
        f"/api/products/{product.uuid}/upload-image",
        data={},
        **staff_auth_headers
    )
    assert response.status_code == 422
