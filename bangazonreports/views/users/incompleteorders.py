"""Module for generating games by user report"""
import sqlite3
from django.shortcuts import render
from bangazonapi.models import Customer
from bangazonreports.views import Connection


def incomplete_orders_list(request):
    """Function to build an HTML report of games by user"""
    if request.method == 'GET':
        # Connect to project database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Query for all games, with related user info.
            db_cursor.execute("""
                SELECT
                    o.id orderId,
                    u.first_name || ' ' || u.last_name AS fullName,
                    SUM(p.price) AS totalCost
                FROM 
                    bangazonapi_order o
                JOIN 
                    bangazonapi_orderproduct op ON o.id = op.order_id
                JOIN 
                    bangazonapi_product p ON op.product_id = p.id
                JOIN 
                    bangazonapi_customer c ON o.customer_id = c.id
                JOIN 
                    auth_user u ON u.id = c.user_id
                WHERE 
                    payment_type_id IS NULL
                GROUP BY 
                    o.customer_id
            """)

            dataset = db_cursor.fetchall()

            incomplete_orders_by_cust = []

            for row in dataset:
                incompleteOrder = {}
                incompleteOrder["orderId"] = row["orderId"]
                incompleteOrder["fullName"] = row["fullName"]
                incompleteOrder["totalCost"] = row['totalCost']

                incomplete_orders_by_cust.append(incompleteOrder)

        # Get only the values from the dictionary and create a list from them
        incomplete_cust_orders = incomplete_orders_by_cust

        # Specify the Django template and provide data context
        template = 'users/incomplete_orders.html'
        context = {
            'incomplete_orders_list': incomplete_cust_orders
        }

        return render(request, template, context)