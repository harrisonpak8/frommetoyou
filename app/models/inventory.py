from flask import current_app as app


class Inventory:
    def __init__(self, sellerID, productID, productname, quantity):
        self.sellerID = sellerID
        self.productID = productID
        self.productname = productname
        self.quantity = quantity

#return inventory of an inputted seller ID
    @staticmethod
    def get_seller(sellerID):
        rows = app.db.execute('''
SELECT sellerID, productID, productname, quantity
FROM Inventory
WHERE sellerID = :sellerID
''',
                              sellerID=sellerID)
        return [Inventory(*row) for row in rows]

    @staticmethod
    def get_sid(pid):
        rows = app.db.execute('''
SELECT sellerID
FROM Inventory
WHERE productID = :pid
''',
                            pid=pid)
        return int(rows[0][0])
    
#Enter seller ID and product ID to delete a product from a sellers inventory
    @staticmethod
    def delete_inventory(sellerID, productID):
        rows = app.db.execute("""
DELETE FROM Inventory
WHERE sellerID = :sellerID and productID = :productID
""",
                              sellerID = sellerID, productID = productID)
        return None
    
#Enter seller ID and product ID to add a product to a sellers inventory
    @staticmethod
    def add_inventory(sellerID, productID, productname, quantity):
        rows = app.db.execute("""
INSERT INTO Inventory(sellerID, productID, productname, quantity)
Values(:sellerID, :productID, :productname, :quantity)
""",
                              sellerID = sellerID, productID = productID, productname=productname, quantity=quantity)
        return None
    
    @staticmethod
    def updateQuantity(sellerID, productID, quantity, productname):
        rows = app.db.execute('''
UPDATE Inventory
SET quantity = :quantity, productname = :productname
WHERE sellerID = :sellerID and productID = :productID
''',
                              sellerID = sellerID, productID = productID, quantity = quantity, productname=productname)
        return None