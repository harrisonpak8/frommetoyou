\COPY Users FROM 'Users.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.users_id_seq',
                         (SELECT MAX(id)+1 FROM Users),
                         false);
\COPY Seller FROM 'Seller.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.seller_id_seq',
                         (SELECT MAX(id)+1 FROM Seller),
                         false);

\COPY Products FROM 'Products.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.products_id_seq',
                         (SELECT MAX(id)+1 FROM Products),
                         false);

/* \COPY Purchases FROM 'Purchases.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.purchases_id_seq',
                         (SELECT MAX(id)+1 FROM Purchases),
                         false); */

\COPY Inventory FROM 'Inventory.csv' WITH DELIMITER ',' NULL '' CSV
\COPY Purchases FROM 'Purchases.csv' WITH DELIMITER ',' NULL '' CSV

\COPY P_Reviews FROM 'P_Reviews.csv' WITH DELIMITER ',' NULL '' CSV

\COPY S_Reviews FROM 'S_Reviews.csv' WITH DELIMITER ',' NULL '' CSV

\COPY Carts FROM 'Carts.csv' WITH DELIMITER ',' NULL '' CSV

\COPY Orders FROM 'Orders.csv' WITH DELIMITER ',' NULL '' CSV

\COPY Conversations FROM 'Conversations.csv' WITH DELIMITER ',' NULL '' CSV

\COPY Messages FROM 'Messages.csv' WITH DELIMITER ',' NULL '' CSV