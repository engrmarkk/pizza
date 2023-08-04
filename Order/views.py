from flask_restx import Resource, Namespace, fields, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from http import HTTPStatus
from ..models.orders import Order
from ..models.users import User
from enum import Enum
from ..utils import db


order_namespace = Namespace("orders", description="a namespace for placing order")

order_model = order_namespace.model(
    "Order",
    {
        "id": fields.Integer(description="An ID"),
        "Size": fields.String(
            description="Size of order",
            required=True,
            enum=["SMALL", "MEDIUM", "LARGE", "EXTRA_LARGE"],
        ),
        "order_status": fields.String(
            description="The status of the Order",
            required=True,
            enum=["PENDING", "IN_TRANSIT", "DELIVERED"],
        ),
        "quantity": fields.Integer(required=True, description='The quantity'),
    },
)


@order_namespace.route("/orders")
class OrderGetCreate(Resource):
    @order_namespace.marshal_with(order_model)
    @jwt_required()
    def get(self):
        """
        Get all orders
        """
        orders = Order.query.all()

        return orders, 200

    @order_namespace.expect(order_model)
    @order_namespace.marshal_with(order_model)
    @jwt_required()
    def post(self):
        """
        place an order
        """

        username = get_jwt_identity()
        print(f'Here is the username {username}')

        current_user = User.query.filter_by(username=username).first()

        data = order_namespace.payload
        print(data['quantity'])

        new_order = Order(
            Size = data["size"],
            quantity = data["quantity"],
            flavour = data["flavour"]
        )

        new_order.user = current_user.id

        new_order.save()

        return new_order, 201


@order_namespace.route("/order/<int:order_id>")
class GetUpdateDelete(Resource):
    @order_namespace.marshal_with(order_model)
    @jwt_required()
    def get(self, order_id):
        """
        Retrieve an order by id
        """

        order = Order.query.get(order_id)
        if not order:
            abort(404, message='Not found')

        return order, HTTPStatus.OK

    def put(self, order_id):
        """
        Retrieve an order by id

        """
        pass

    def put(self, order_id):
        """
        Update an order with id

        """
        pass

    def delete(self, order_id):
        """
        Delete an order with id

        """
        pass


@order_namespace.route("/user/<int:user_id>/order/<int:order>")
class UserOrders(Resource):
    def get(self, user_id):
        """
        Get all orders by a specific.
        """

        user = User.get_by_id(user_id)

        Orders = user.Orders


@order_namespace.route("/order/status/<int:order_id>")
class UpdateOrdersStatus(Resource):
    def get(self, user_id):
        """
        update an order's status
        """
        pass
