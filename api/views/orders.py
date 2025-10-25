from uuid import UUID

from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.errors import HttpError
from ninja.errors import ValidationError as NinjaValidationError

from accounts.deps import AuthBearer
from api.models import Order, DeliveryAddress
from api.schemas.orders import OrderOut, OrderAdminOut, OrderIn, OrderInUpdate
from api.utils import staff_required

router = Router(tags=["orders"], auth=AuthBearer())


# --- READ ALL ---
@router.get("/", response=list[OrderOut])
def list_orders(request):
    """List all orders"""
    user = request.auth
    return Order.objects.filter(user=user).all()


# --- READ ALL (staff only)---
@router.get("/admin", response=list[OrderAdminOut])
def list_orders_staff(request):
    """List all orders from all users to staff"""
    user = request.auth
    if not user.is_staff:
        raise HttpError(403, "Not authorized")
    return Order.objects.all()


# --- READ ONE ---
@router.get("/{order_uuid}", response=OrderOut)
def get_order(request, order_uuid: UUID):
    """Get an order by uuid"""
    user = request.auth
    return get_object_or_404(Order, user=user, uuid=order_uuid)


# --- READ ONE (staff only)---
@router.get("/admin/{order_uuid}", response=OrderAdminOut)
def get_order_staff(request, order_uuid: UUID):
    """Get an order by uuid to staff"""
    user = request.auth
    if not user.is_staff:
        raise HttpError(403, "Not authorized")
    return get_object_or_404(Order, uuid=order_uuid)


# --- CREATE ---
@router.post("/", response=OrderOut)
def create_order(request, data: OrderIn):
    """Create a new order"""
    user = request.auth
    delivery_address = get_object_or_404(DeliveryAddress, user=user, uuid=data.delivery_address_uuid)
    with transaction.atomic():
        order = Order.objects.create(
            payment_method=data.payment_method,
            delivery_address=delivery_address,
            user=user,
        )
        try:
            order.full_clean()
            order.save()
            return order
        except ValidationError as e:
            raise NinjaValidationError(e.message_dict)


# --- UPDATE (staff only) ---
@staff_required
@router.put("/{order_uuid}", response=OrderOut)
def update_order_staff(request, order_uuid: str, data: OrderInUpdate):
    """Update an order (only staff)"""
    order = get_object_or_404(Order, uuid=order_uuid)
    for field, value in data.dict(exclude_unset=True).items():
        setattr(order, field, value)
    try:
        order.full_clean()
        order.save()
        return order
    except ValidationError as e:
        raise NinjaValidationError(e.message_dict)


# --- DELETE (staff only) ---
@staff_required
@router.delete("/{order_uuid}")
def delete_order_staff(request, order_uuid: str):
    """Delete an order (only staff)"""
    order = get_object_or_404(Order, uuid=order_uuid)
    order.soft_delete()
    return HttpResponse(status=204)
