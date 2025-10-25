from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import get_object_or_404
from ninja import Router

from accounts.deps import AuthBearer
from api.models import OrderItem, Order, Product
from api.schemas.orderitems import OrderItemIn, OrderItemOut, ItemOut
from ninja.errors import ValidationError as NinjaValidationError, HttpError

router = Router(tags=["order-items"], auth=AuthBearer())


def build_order_item_response(order: Order) -> OrderItemOut:
    """Helper to mount the OrderItemOut schema"""

    products = [
        ItemOut(
            uuid=item.product.uuid,
            name=item.product.name,
            description=item.product.description,
            price=float(item.unit_price),
            image=item.product.image.url if item.product.image else None,
            quantity=item.quantity
        )
        for item in order.items.all()
    ]

    return OrderItemOut(
        order_uuid=order.uuid,
        order_number=order.order_number,
        order_date=order.order_date,
        payment_method=order.payment_method,
        status=order.status,
        delivery_address=order.delivery_address,
        products=products
    )


# --- CREATE ---
@router.post("/", response=OrderItemOut)
def create_order_item(request, data: OrderItemIn):
    """Create a new item in an order"""
    user = request.auth
    order = get_object_or_404(Order, user=user, uuid=data.order_uuid)
    if order.status not in (Order.OrderStatus.DRAFT, Order.OrderStatus.PENDING):
        raise HttpError(400, f"Order cannot add items at '{order.status}' status")
    product = get_object_or_404(Product, uuid=data.product_uuid)
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
