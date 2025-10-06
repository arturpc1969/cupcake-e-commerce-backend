import os
from uuid import UUID, uuid4

from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from ninja import Router, File, UploadedFile, Form
from ninja.errors import ValidationError as NinjaValidationError

from accounts.deps import AuthBearer
from api.models import Product
from api.schemas.product import ProductOut
from api.utils import staff_required

router = Router(tags=["products"])


# --- Auxiliar function to save image ---
def save_uploaded_image(image: UploadedFile) -> str:
    ext = image.name.split('.')[-1]
    filename = f"{uuid4()}.{ext}"
    path = os.path.join('media', 'products', filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, 'wb+') as destination:
        for chunk in image.chunks():
            destination.write(chunk)

    return f"products/{filename}"


# --- READ ALL (public) ---
@router.get("/", response=list[ProductOut])
def list_products(request):
    """List all products"""
    return Product.objects.all()


# --- UPDATE (staff only) ---
@staff_required
@router.put("/{uuid}", response=ProductOut, auth=AuthBearer())
def update_product(
    request,
    uuid: str,
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    image: UploadedFile | None = File(None),
):
    """Update a product (only staff)"""
    product = get_object_or_404(Product, uuid=uuid)

    product.name = name
    product.description = description
    product.price = price

    if image:
        image_path = save_uploaded_image(image)
        product.image = image_path

    try:
        product.full_clean()
        product.save()
        return product
    except ValidationError as e:
        raise NinjaValidationError(e.message_dict)


# --- READ ONE (public) ---
@router.get("/{uuid}", response=ProductOut)
def get_product(request, uuid: UUID):
    """Get a product by UUID"""
    return get_object_or_404(Product, uuid=uuid)


# --- CREATE (staff only) ---
@staff_required
@router.post("/", response=ProductOut, auth=AuthBearer())
def create_product(
    request,
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    image: UploadedFile | None = File(None),
):
    """Create a new product (only staff)"""
    image_path = save_uploaded_image(image) if image else None
    product = Product(name=name,
                      description=description,
                      price=price,
                      image=image_path)
    try:
        product.full_clean()
        product.save()
        return product
    except ValidationError as e:
        raise NinjaValidationError(e.message_dict)


# --- DELETE (staff only) ---
@staff_required
@router.delete("/{uuid}", auth=AuthBearer())
def delete_product(request, uuid: str):
    """Delete a product (only staff)"""
    product = get_object_or_404(Product, uuid=uuid)
    product.soft_delete()
    return HttpResponse(status=204)


# --- Image upload ---
@staff_required
@router.post("/{product_uuid}/upload-image", response=ProductOut, auth=AuthBearer())
def upload_product_image(request, product_uuid: UUID, image: UploadedFile = File(...)):
    """Make upload or replace the product image"""
    product = get_object_or_404(Product, uuid=product_uuid)
    image_path = save_uploaded_image(image) if image else None
    product.image = image_path
    try:
        product.full_clean()
        product.save()
        return product
    except ValidationError as e:
        raise NinjaValidationError(e.message_dict)
