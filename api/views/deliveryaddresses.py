from uuid import UUID

from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.errors import HttpError
from ninja.errors import ValidationError as NinjaValidationError

from accounts.deps import AuthBearer
from api.models import DeliveryAddress
from api.schemas.deliveryaddresses import DeliveryAddressOut, DeliveryAddressIn

router = Router(tags=["delivery addresses"], auth=AuthBearer())


# --- READ ALL ---
@router.get("/", response=list[DeliveryAddressOut])
def list_delivery_addresses(request):
    """List all delivery addresses"""
    user = request.auth
    if user.is_staff:
        return DeliveryAddress.objects.all()
    return DeliveryAddress.objects.filter(user=user).all()


# --- READ ONE ---
@router.get("/{uuid}", response=DeliveryAddressOut)
def get_delivery_address(request, uuid: UUID):
    """Get a delivery address by UUID"""
    user = request.auth
    delivery_address = get_object_or_404(DeliveryAddress, uuid=uuid)
    if not user.is_staff and delivery_address.user != user:
        raise HttpError(403, "You do not have permission to access this delivery address.")
    return delivery_address


# --- CREATE ---
@router.post("/", response=DeliveryAddressOut)
def create_delivery_address(request, data: DeliveryAddressIn):
    """Create a new delivery address"""
    user = request.auth
    delivery_address = DeliveryAddress(address_name=data.address_name,
                                       address_description=data.address_description,
                                       city=data.city,
                                       state=data.state,
                                       zip_code=data.zip_code,
                                       user=user)
    try:
        delivery_address.full_clean()
        delivery_address.save()
        return delivery_address
    except ValidationError as e:
        raise NinjaValidationError(e.message_dict)


# --- UPDATE ---
@router.put("/{uuid}", response=DeliveryAddressOut)
def update_delivery_address(request, uuid: str, data: DeliveryAddressIn):
    """Update a delivery address"""
    delivery_address = get_object_or_404(DeliveryAddress, uuid=uuid, user=request.auth)
    for field, value in data.dict(exclude_unset=True).items():
        setattr(delivery_address, field, value)
    try:
        delivery_address.full_clean()
        delivery_address.save()
        return delivery_address
    except ValidationError as e:
        raise NinjaValidationError(e.message_dict)


# --- DELETE ---
@router.delete("/{uuid}")
def delete_delivery_address(request, uuid: str):
    """Delete a delivery address"""
    delivery_address = get_object_or_404(DeliveryAddress, uuid=uuid, user=request.auth)
    delivery_address.soft_delete()
    return HttpResponse(status=204)
