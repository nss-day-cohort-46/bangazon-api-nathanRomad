"""Module for generating games by user report"""
import sqlite3
from django.shortcuts import render
from bangazonapi.models import Customer
from bangazonreports.views import Connection


def inexpensive_products_list(request):
    """Function to build an HTML report of games by user"""
    if request.method == 'GET':
        # Connect to project database
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Query for all games, with related user info.
            db_cursor.execute("""
                SELECT
                    p.price AS price,
                    p.name AS name
                FROM bangazonapi_product p
                WHERE p.price < 999
                ORDER BY p.name
            """)

            dataset = db_cursor.fetchall()

            inexpensive_products = []

            for row in dataset:
                inexpensiveProduct = {}
                inexpensiveProduct["name"] = row["name"]
                inexpensiveProduct["price"] = row["price"]

                inexpensive_products.append(inexpensiveProduct)

        # Specify the Django template and provide data context
        template = 'users/inexpensive_products.html'
        context = {
            'inexpensive_products_list': inexpensive_products
        }

        return render(request, template, context)