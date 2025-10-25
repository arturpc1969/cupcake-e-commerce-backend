from uuid import UUID

from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.errors import ValidationError as NinjaValidationError, HttpError

from accounts.deps import AuthBearer
from api.models import OrderItem, Order, Product
from api.schemas.orderitems import OrderItemIn, OrderItemOut, OrderItemAdminOut
from api.services.orderitems import build_order_item_response, build_order_item_response_staff

router = Router(tags=["order-items"], auth=AuthBearer())


# --- CREATE ---
@router.post("/", response=OrderItemOut)
def create_order_item(request, data: OrderItemIn):
    """Create a new item in an order"""
    user = request.auth
    order = get_object_or_404(Order, user=user, uuid=data.order_uuid)

    if order.status not in (Order.OrderStatus.DRAFT, Order.OrderStatus.PENDING):
        raise HttpError(400, f"Order cannot add items at '{order.status}' status")

    product = get_object_or_404(Product, uuid=data.product_uuid)

    if OrderItem.objects.filter(order=order, product=product).exists():
        raise HttpError(400, f"This product already exist in this order.")

    with transaction.atomic():
        order_item = OrderItem(
            order=order,
            product=product,
            quantity=data.quantity,
            unit_price=product.price,
        )
        try:
            order_item.full_clean()
            order_item.save()
            return build_order_item_response(order)
        except ValidationError as e:
            raise NinjaValidationError(e.message_dict)


# --- READ ALL ---
@router.get("/", response=list[OrderItemOut])
def list_order_items(request):
    """List all order with items"""
    user = request.auth
    orders = Order.objects.filter(user=user).all()
    order_items_out = [build_order_item_response(order) for order in orders]
    return order_items_out


# --- READ ALL (staff only)---
@router.get("/admin", response=list[OrderItemAdminOut])
def list_order_items_staff(request):
    """List all order with items from all users to staff"""
    user = request.auth
    if not user.is_staff:
        raise HttpError(403, "Not authorized")
    orders = Order.objects.all()
    order_items_out = [build_order_item_response_staff(order) for order in orders]
    return order_items_out


# --- READ ONE ---
@router.get("/{order_uuid}", response=OrderItemOut)
def get_order_item(request, order_uuid: UUID):
    """Get an order with items by uuid"""
    user = request.auth
    order = get_object_or_404(Order, user=user, uuid=order_uuid)
    return build_order_item_response(order)


# --- READ ONE (staff only)---
@router.get("/admin/{order_uuid}", response=OrderItemAdminOut)
def get_order_item_staff(request, order_uuid: UUID):
    """Get an order with items by uuid to staff"""
    user = request.auth
    if not user.is_staff:
        raise HttpError(403, "Not authorized")
    order = get_object_or_404(Order, uuid=order_uuid)
    return build_order_item_response_staff(order)


# --- UPDATE ---
@router.put("/", response=OrderItemOut)
def update_order_item(request, data: OrderItemIn):
    """Update an order item"""
    user = request.auth
    order = get_object_or_404(Order, user=user, uuid=data.order_uuid)
    product = get_object_or_404(Product, uuid=data.product_uuid)
    order_item = get_object_or_404(OrderItem, order=order, product=product)
    for field, value in data.dict(exclude_unset=True).items():
        setattr(order_item, field, value)
    try:
        order_item.full_clean()
        order_item.save()
        return build_order_item_response(order)
    except ValidationError as e:
        raise NinjaValidationError(e.message_dict)
