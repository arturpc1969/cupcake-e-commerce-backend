from decimal import Decimal
from uuid import UUID

from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from ninja import Router, File, UploadedFile, Form
from ninja.errors import ValidationError as NinjaValidationError

from accounts.deps import AuthBearer
from api.models import Product
from api.schemas.products import ProductOut
from api.utils import staff_required

router = Router(tags=["products"])


# --- READ ALL (public) ---
@router.get("/", response=list[ProductOut])
def list_products(request):
    """List all products"""
    return Product.objects.all()


# --- UPDATE (staff only) ---
@router.put("/{uuid}", response=ProductOut, auth=AuthBearer())
@staff_required
def update_product(
    request,
    uuid: str,
    name: str = Form(...),
    description: str = Form(...),
    price: Decimal = Form(...),
    promotion: bool = Form(...),
    image: UploadedFile | None = File(None),
):
    """Update a product (only staff)"""
    product = get_object_or_404(Product, uuid=uuid)

    product.name = name
    product.description = description
    product.price = price
    product.promotion = promotion

    if image:
        product.image = image  # Django + Cloudinary fazem o upload automaticamente

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
@router.post("/", response=ProductOut, auth=AuthBearer())
@staff_required
def create_product(
    request,
    name: str = Form(...),
    description: str = Form(...),
    price: Decimal = Form(...),
    promotion: bool = Form(...),
    image: UploadedFile | None = File(None),
):
    """Create a new product (only staff)"""
    product = Product(name=name,
                      description=description,
                      price=price,
                      promotion=promotion)
                      # image=image_path)

    if image:
        product.image = image  # Django + Cloudinary fazem o upload automaticamente

    try:
        product.full_clean()
        product.save()
        return product
    except ValidationError as e:
        raise NinjaValidationError(e.message_dict)


# --- DELETE (staff only) ---
@router.delete("/{uuid}", auth=AuthBearer())
@staff_required
def delete_product(request, uuid: str):
    """Delete a product (only staff)"""
    product = get_object_or_404(Product, uuid=uuid)
    product.soft_delete()
    return HttpResponse(status=204)


# --- Image upload ---
@router.post("/{product_uuid}/upload-image", response=ProductOut, auth=AuthBearer())
@staff_required
def upload_product_image(request, product_uuid: UUID, image: UploadedFile = File(...)):
    """Make upload or replace the product image"""
    product = get_object_or_404(Product, uuid=product_uuid)
    product.image = image  # Django + Cloudinary fazem o upload automaticamente
    try:
        product.full_clean()
        product.save()
        return product
    except ValidationError as e:
        raise NinjaValidationError(e.message_dict)
