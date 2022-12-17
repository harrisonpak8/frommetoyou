from flask import current_app as app


class Fulfillments:
    def __init__(self, oid, pid, quantity, firstname, lastname, address, time_purchased, fulfilled):
        self.oid = oid
        self.pid = pid
        self.quantity = quantity
        self.firstname = firstname
        self.lastname = lastname
        self.address = address
        self.time_purchased = time_purchased
        self.fulfilled = fulfilled

#return orders of current seller ID
    @staticmethod
    def get_orders(sid):
        rows = app.db.execute('''
SELECT oid, pid, quantity, firstname, lastname, address, time_purchased, fulfilled
FROM Orders o, Users u
WHERE sid = :sid AND uid = id
ORDER BY time_purchased DESC
''',
                              sid=sid)
        return [Fulfillments(*row) for row in rows]
    
    
    @staticmethod
    def to_true(sid, oid):
        rows = app.db.execute('''
UPDATE Orders
SET fulfilled = True
WHERE sid = :sid and oid = :oid
''',
                            sid=sid, oid=oid)
        return None
    
    @staticmethod
    def to_false(sid, oid):
        rows = app.db.execute('''
UPDATE Orders
SET fulfilled = False
WHERE sid = :sid and oid = :oid
''',
                            sid=sid, oid=oid)
        return None