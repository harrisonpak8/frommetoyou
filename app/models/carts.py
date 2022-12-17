from flask import current_app as app
from datetime import datetime

class Cart:
    def __init__(self, uid, pid, sid, quantity, unit_price):
        self.uid = uid
        self.pid = pid
        self.sid = sid
        self.quantity = quantity
        self.unit_price = unit_price

    @staticmethod
    def num_items_in_cart(uid):
        rows=app.db.execute('''
SELECT SUM(quantity)
FROM Carts
WHERE uid=:uid
''',
                              uid=uid)
        if rows:
            return rows[0][0]
        else:
            return 0

    @staticmethod
    def subtotal(uid):
        rows=app.db.execute('''
SELECT SUM(unit_price*quantity)
FROM Carts
WHERE uid=:uid
''',
                              uid=uid)
        if len(rows) > 0:
            return rows[0][0]
        else:
            return 0

    @staticmethod
    def get_cart(uid):
        rows = app.db.execute('''
SELECT uid, pid, sid, quantity, unit_price
FROM Carts
WHERE uid = :uid
''',
                              uid=uid)
        return [Cart(*row) for row in rows]
    
    @staticmethod
    def delete_cart_item(uid, pid):
        rows = app.db.execute('''
DELETE FROM Carts
WHERE uid = :uid
  AND pid = :pid
''', 
                              uid=uid, pid=pid)
        return None
        
    @staticmethod
    def insert_into_cart(uid, pid, sid, productname, quantity, unit_price):
        rows = app.db.execute('''
INSERT INTO Carts(uid, pid, sid, productname, quantity, unit_price)
Values(:uid, :pid, :sid, :productname, :quantity, :unit_price)
''',
                              uid=uid, pid=pid, sid=sid, productname=productname, quantity=quantity, unit_price=unit_price)
        return None
        
    @staticmethod
    def update_quantity(uid, pid, quantity):
        rows = app.db.execute('''
UPDATE Carts
SET quantity = :quantity
WHERE uid = :uid
  AND pid = :pid
''', 
                              uid=uid, pid=pid, quantity=quantity)
        return None

    @staticmethod
    def send_to_orders(oid, uid, date, fulfilled, subtotal):
        ''' STEP 1: Insert into the Orders table the automatically generated oid, uid, pid, sid, quantity, unit_price, current timestamp
                    and False for fulfilled '''

        rows = app.db.execute('''
INSERT INTO Orders(oid, uid, pid, sid, quantity, unit_price, date, fulfilled)
SELECT uid, pid, sid, quantity, unit_price
FROM Carts
WHERE uid=:uid
''',
                            oid=oid, uid=uid, date=date, fulfilled=fulfilled)

        ''' STEP 2: Add the (unit_price * quantity) of each item to the Seller's balance who sells that item'''

        rows2 = app.db.execute('''
UPDATE Sellers
SET balance = balance + (unit_price * quantity)
FROM Sellers s, Carts c
WHERE c.uid = :uid
  AND s.uid = c.sid
''',
                            subtotal=subtotal, uid=uid)

        ''' STEP 3: Subtract the subtotal of the User's cart from the previous balance of the User. '''

        rows3 = app.db.execute('''
UPDATE Users
SET balance = balance - :subtotal
WHERE uid =:uid
''',
                            subtotal=subtotal, uid=uid)
        ''' STEP 4: Subtract from Inventory the amount of each product bought. '''
        
        rows4 = app.db.execute('''
UPDATE Inventory
SET i.quantity = i.quantity - c.quantity
FROM Carts c, Inventory i
WHERE c.uid = :uid
  AND c.pid = i.productID
'''
)

        ''' STEP 5: Delete the items from User's cart. '''

        rows5 = app.db.execute('''
DELETE FROM Carts
WHERE uid=:uid
''',
                            uid=uid)
        return None