import json
from rest_framework import status
from rest_framework.test import APITestCase


class OrderTests(APITestCase):
    def setUp(self) -> None:
        """
        Create a new account and create sample category
        """
        url = "/register"
        data = {"username": "steve", "password": "Admin8*", "email": "steve@stevebrownlee.com",
                "address": "100 Infinity Way", "phone_number": "555-1212", "first_name": "Steve", "last_name": "Brownlee"}
        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)
        self.token = json_response["token"]
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Create a product category
        url = "/productcategories"
        data = {"name": "Sporting Goods"}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data, format='json')

        # Create a product
        url = "/products"
        data = { "name": "Kite", "price": 14.99, "quantity": 60, "description": "It flies high", "category_id": 1, "location": "Pittsburgh" }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Create a payment type
        url = "/paymenttypes"
        data = {
            "merchant_name": "Jake",
            "account_number": "123",
            "expiration_date": "2021-01-01",
            "create_date": "2021-01-01"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)



    def test_add_product_to_order(self):
        """
        Ensure we can add a product to an order.
        """
        # Add product to order
        url = "/cart"
        data = { "product_id": 1 }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Get cart and verify product was added
        url = "/cart"
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(url, None, format='json')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["id"], 1)
        self.assertEqual(json_response["size"], 1)
        self.assertEqual(len(json_response["lineitems"]), 1)


    def test_remove_product_from_order(self):
        """
        Ensure we can remove a product from an order.
        """
        # Add product
        self.test_add_product_to_order()

        # Remove product from cart
        url = "/cart/1"
        data = { "product_id": 1 }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Get cart and verify product was removed
        url = "/cart"
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(url, None, format='json')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["size"], 0)
        self.assertEqual(len(json_response["lineitems"]), 0)

    # TODO: Complete order by adding payment type
    def test_complete_order(self):
        """
            Ensure a new line item is added to closed orders
        """
        self.test_add_product_to_order()
        url = "/orders/1"

        #to close an order it must have a payment type
        data = {
            "payment_type": 1
        }
        #POST data to defined URL in JSON format
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        #assert the data posted
        #checking to see the order has the correct payment type
        response = self.client.get(url)
        json_response = json.loads(response.content)
        self.assertEqual(json_response['payment_type'], "http://testserver/paymenttypes/1")

    # TODO: New line item is not added to closed order // #10
    def test_new_order(self):
        """
            Ensure a new line item is added to closed orders
        """
        self.test_add_product_to_order()
        url = "/orders/1"

        #to close an order it must have a payment type
        data = {
            "payment_type": 1
        }
        #POST data to defined URL in JSON format
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        #assert the data posted
        #checking to see the order has the correct payment type
        response = self.client.get(url)
        json_response = json.loads(response.content)
        self.assertEqual(json_response['payment_type'], "http://testserver/paymenttypes/1")

        #add new line items to cart to test that order was closed and new order is created
        url = "/profile/cart"
        data = { "product_id": 1 }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #assert that the new order has an id of 2
        response = self.client.get(url)
        json_response = json.loads(response.content)
        self.assertEqual(json_response["id"], 2)