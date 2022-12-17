from flask import current_app as app


class Product:
    def __init__(self, id, name, link, price, category, available, descr):
        self.id = id
        self.name = name
        self.link = link
        self.price = price
        self.category = category
        self.available = available
        self.descr = descr

    @staticmethod
    def get(id):
        rows = app.db.execute('''
SELECT id, name, link, price, category, available, descr
FROM Products
WHERE id = :id
''',
                              id=id)
        return Product(*(rows[0])) if rows is not None else None

    @staticmethod
    def get_all(available=True):
        rows = app.db.execute('''
SELECT id, name, link, price, category, available, descr
FROM Products
WHERE available = :available
''',
                              available=available)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_top_k(k):
        rows = app.db.execute('''
SELECT id, name, link, price, category, available, descr
FROM Products
ORDER BY price DESC
LIMIT :k
''',
                              k=k)
        return [Product(*row) for row in rows]


    @staticmethod
    def order_d():
        rows = app.db.execute('''
SELECT id, name, link, price, category, available, descr
FROM Products
ORDER BY price DESC
''',
                              )
        return [Product(*row) for row in rows]

    @staticmethod
    def order_a():
        rows = app.db.execute('''
SELECT id, name, link, price, category, available, descr
FROM Products
ORDER BY price ASC
''',
                              )
        return [Product(*row) for row in rows]

    @staticmethod
    def get_by_cat(cat):
        rows = app.db.execute('''
SELECT id, name, link, price, category, available, descr
FROM Products
WHERE category = :cat
''',
                              cat=cat)
        return [Product(*row) for row in rows]

    @staticmethod
    def get_by_kw(kw):
        rows = app.db.execute('''
SELECT id, name, link, price, category, available, descr
FROM Products
WHERE name LIKE Concat('%', :kw, '%')
''',
                              kw=kw)
        return [Product(*row) for row in rows]

    @staticmethod
    def delete_product(pid, sid):
        rows = app.db.execute("""
DELETE FROM Products
WHERE sid = :sid and id = :pid
""",
                              sid = sid, pid = pid)
        return None  
          
    @staticmethod
    def add_product(id, sid, name, descr, category, price, available):
        rows = app.db.execute("""
INSERT INTO Products(id, sid, name, descr, category, price, available)
Values(:id, :sid, :name, :descr, :category, :price, :available)
""",
                                id=id, sid=sid, name=name, descr=descr, category=category, price=price, available=available)
        return None

    @staticmethod
    def edit_product(id, sid, name, descr, price):
        rows = app.db.execute("""
UPDATE Products
SET name = :name, descr = :descr, price = :price
WHERE id = :id and sid =:sid
        """,
                                id=id, sid=sid, name=name, descr=descr, price=price)
        return None

    @staticmethod
    def get_maxid():
        rows = app.db.execute("""
SELECT id FROM Products
WHERE id = (SELECT MAX(id) FROM Products)
LIMIT 1
""",)
        return int(rows[0][0])