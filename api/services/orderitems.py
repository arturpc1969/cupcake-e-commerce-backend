from api.models import Order
from api.schemas.orderitems import OrderItemOut, ItemOut, OrderItemAdminOut


def build_order_item_response(order: Order) -> OrderItemOut:
    """Helper to mount the OrderItemOut schema"""

    products = [
        ItemOut(
            uuid=item.product.uuid,
            name=item.product.name,
            description=item.product.description,
            price=float(item.unit_price),
            promotion=item.product.promotion,
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


def build_order_item_response_staff(order: Order) -> OrderItemAdminOut:
    """Helper to mount the OrderItemOut schema for staff response"""

    products = [
        ItemOut(
            uuid=item.product.uuid,
            name=item.product.name,
            description=item.product.description,
            price=float(item.unit_price),
            promotion=item.product.promotion,
            image=item.product.image.url if item.product.image else None,
            quantity=item.quantity
        )
        for item in order.items.all()
    ]

    return OrderItemAdminOut(
        order_uuid=order.uuid,
        order_number=order.order_number,
        order_date=order.order_date,
        payment_method=order.payment_method,
        status=order.status,
        delivery_address=order.delivery_address,
        products=products,
        user=order.user
    )
