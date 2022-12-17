from flask import current_app as app


class Purchase:
    def __init__(self, oid, uid, pid, time_purchased, quantity, unit_price, fulfilled):
        self.oid = oid
        self.uid = uid
        self.pid = pid
        self.time = time_purchased
        self.quantity = quantity
        self.price = unit_price
        self.status = fulfilled

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT oid, uid, pid, time_purchased, quantity, unit_price, fulfilled
FROM Orders
WHERE oid = :id
''',
                              id=id)
        return Purchase(*(rows[0])) if rows else None

    @staticmethod
    def get_all_by_uid_since(uid, since):
        rows = app.db.execute('''
SELECT oid, uid, pid, time_purchased, quantity, unit_price, fulfilled
FROM Orders
WHERE uid = :uid
AND time_purchased >= :since
ORDER BY time_purchased DESC
''',
                              uid=uid,
                              since=since)
        return [Purchase(*row) for row in rows]

    @staticmethod
    def get_all_by_uid(uid):
        rows = app.db.execute('''
SELECT oid, uid, pid, time_purchased, quantity, unit_price, fulfilled
FROM Orders
WHERE uid = :uid
ORDER BY time_purchased DESC
''',
                            uid=uid)
        return [Purchase(*row) for row in rows]
