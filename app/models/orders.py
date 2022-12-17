from flask import current_app as app
from datetime import datetime

class Order:
    def __init__(self, oid, uid, pid, sid, quantity, unit_price, time_purchased, fulfilled):
        self.oid = oid
        self.uid = uid
        self.pid = pid
        self.sid = sid
        self.quantity = quantity
        self.unit_price = unit_price
        self.time_purchased = time_purchased
        self.fulfilled = fulfilled

    @staticmethod
    def get_order_ids(uid):
        rows=app.db.execute('''
SELECT DISTINCT oid
FROM Orders
WHERE uid=:uid
ORDER BY oid DESC
''',
                             uid=uid)
            
        return list([Order(*row) for row in rows])


    @staticmethod
    def get_orders(uid):
        rows=app.db.execute('''
SELECT oid, uid, pid, sid, quantity, unit_price, time_purchased, fulfilled
FROM Orders
WHERE uid=:uid
ORDER BY time_purchased DESC
''',
                             uid=uid)

        return [Order(*row) for row in rows] 
    