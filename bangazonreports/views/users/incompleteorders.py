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
                    c.id custId,
                    u.first_name || ' ' || u.last_name AS fullName,
                    SUM(p.price) AS totalCost
                FROM
                    bangazonapi_customer c
                JOIN
                    auth_user u ON c.id = u.id
                JOIN 
                    bangazonapi_order o ON o.customer_id = custId
                JOIN 
                    bangazonapi_orderproduct op ON o.id = op.order_id
                JOIN 
                    bangazonapi_product p ON op.product_id = p.id
                GROUP BY 
                    custId
            """)

            dataset = db_cursor.fetchall()

            favseller_by_cust = {}

            for row in dataset:
                # Crete a Game instance and set its properties
                favorite = Customer()
                favorite.id = row['seller']
                favorite.name = row['sellerName']

                # Store the user's id
                uid = row["custId"]

                # If the user's id is already a key in the dictionary...
                if uid in favseller_by_cust:

                    # Add the current game to the `games` list for it
                    favseller_by_cust[uid]['seller'].append(favorite)

                else:
                    # Otherwise, create the key and dictionary value
                    favseller_by_cust[uid] = {}
                    favseller_by_cust[uid]["id"] = uid
                    favseller_by_cust[uid]["fullName"] = row["fullName"]
                    favseller_by_cust[uid]["seller"] = [favorite]

        # Get only the values from the dictionary and create a list from them
        list_of_users_with_favs = favseller_by_cust.values()

        # Specify the Django template and provide data context
        template = 'users/favsellerbycust.html'
        context = {
            'favseller_list': list_of_users_with_favs
        }

        return render(request, template, context)