from flask_login import UserMixin
from flask import current_app as app
from werkzeug.security import generate_password_hash, check_password_hash

from .. import login


class User(UserMixin):
    def __init__(self, id, email, firstname, lastname, address):
        self.id = id
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.address = address

    @staticmethod
    def get_by_auth(email, password):
        rows = app.db.execute("""
SELECT password, id, email, firstname, lastname, address
FROM Users
WHERE email = :email
""",
                              email=email)
        if not rows:  # email not found
            return None
        elif not check_password_hash(rows[0][0], password):
            # incorrect password
            return None
        else:
            return User(*(rows[0][1:]))

    @staticmethod
    def email_exists(email):
        rows = app.db.execute("""
SELECT email
FROM Users
WHERE email = :email
""",
                              email=email)
        return len(rows) > 0

    @staticmethod
    def register(email, password, firstname, lastname, address):
        try:
            rows = app.db.execute("""
INSERT INTO Users(email, password, firstname, lastname, address)
VALUES(:email, :password, :firstname, :lastname, :address)
RETURNING id
""",
                                  email=email,
                                  password=generate_password_hash(password),
                                  firstname=firstname, lastname=lastname, address=address)
            id = rows[0][0]
            return User.get(id)
        except Exception as e:
            # likely email already in use; better error checking and reporting needed;
            # the following simply prints the error to the console:
            print(str(e))
            return None

    @staticmethod
    @login.user_loader
    def get(id):
        rows = app.db.execute("""
SELECT id, email, firstname, lastname, address
FROM Users
WHERE id = :id
""",
                              id=id)
        return User(*(rows[0])) if rows else None

    @staticmethod
    def update(id, email, password, firstname, lastname, address):
        rows = app.db.execute("""
UPDATE Users
SET email = :email, password = :password, firstname = :firstname, lastname = :lastname, address = :address
WHERE id = :id
""",
                              id=id, email=email, password=password, firstname=firstname, lastname=lastname,
                              address=address)
        return None
    
    @staticmethod
    def update_ubalance(id, amount):
        rows = app.db.execute("""
UPDATE Users
SET balance = balance + :amount
WHERE id = :id
""",
                              id=id, amount=amount)
        return None

    @staticmethod
    def update_sbalance(uid, amount):
        rows = app.db.execute("""
UPDATE Seller
SET balance = balance + :amount
WHERE uid = :uid
""",
                              uid=uid, amount=amount)
        return None
    
    @staticmethod
    def current_ubalance(id):
        rows = app.db.execute("""
SELECT balance
FROM Users
WHERE id = :id
""",
                              id=id)
        return rows[0][0] if rows else None
    
    @staticmethod
    def current_sbalance(uid):
        rows = app.db.execute("""
SELECT balance
FROM Seller
WHERE uid = :uid
""",
                              uid=uid)
        return rows[0][0] if rows else None

    @staticmethod
    def restore_balance(id, amount):
        rows = app.db.execute("""
UPDATE Users
SET balance = balance - :amount
WHERE id = :id
""",
                              id=id, amount=amount)
        return None