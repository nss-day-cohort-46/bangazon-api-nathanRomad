INSERT INTO bangazonapi_recommendation (customer_id, product_id, recommender_id)
VALUES (4, 1, 5)

SELECT
    c.id custId,
    u.first_name || ' ' || u.last_name AS fullName,
    u.username,
    fav.id favId
FROM
    bangazonapi_customer c
JOIN
    bangazonapi_favorite fav ON c.id = fav.customer_id
JOIN
    auth_user u ON c.id = u.id