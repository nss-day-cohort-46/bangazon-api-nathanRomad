"""Module for generating games by user report"""
import sqlite3
from django.shortcuts import render
from bangazonapi.models import Customer
from bangazonreports.views import Connection


def completed_orders_list(request):
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
                    SUM(p.price) AS totalCost,
                    pay.merchant_name AS payType
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
                JOIN
                    bangazonapi_payment pay ON o.payment_type_id = pay.id
                WHERE 
                    payment_type_id IS NOT NULL
                GROUP BY 
                    o.customer_id
            """)

            dataset = db_cursor.fetchall()

            completed_orders_by_cust = []

            for row in dataset:
                completedOrder = {}
                completedOrder["orderId"] = row["orderId"]
                completedOrder["fullName"] = row["fullName"]
                completedOrder["totalCost"] = row['totalCost']
                completedOrder["payType"] = row['payType']

                completed_orders_by_cust.append(completedOrder)

        # Specify the Django template and provide data context
        template = 'users/completed_orders.html'
        context = {
            'completed_orders_list': completed_orders_by_cust
        }

        return render(request, template, context)