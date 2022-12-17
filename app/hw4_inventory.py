from flask import Flask, render_template, request, flash, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField
from .models.inventory import Inventory
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask import Blueprint


from .models.user import User
from .models.product import Product
from flask_login import login_user, logout_user, current_user

bp = Blueprint('hw4_inventory', __name__)

class InventoryForm(FlaskForm):
    sid_input = StringField('Seller ID')
    submit = SubmitField('Submit')
    
class delete_invForm(FlaskForm):
    pid_input2 = StringField('Product ID', validators=[DataRequired()])
    submit2 = SubmitField('Delete')
    
class add_invForm(FlaskForm):
    productname3 = StringField('Product Name', validators=[DataRequired()])
    descr = StringField("Description", validators=[DataRequired()])
    cat = RadioField('Category', choices=['accessories', 'books', 'clothes', 'decor', 'electronics', 'food', 'games', 'shoes'])
    price = StringField("Price", validators=[DataRequired()])
    quantity3 = StringField('Quantity', validators=[DataRequired()])
    submit3 = SubmitField('Add')
    
class change_invForm(FlaskForm):
    pid_input4 = StringField('Product ID', validators=[DataRequired()])
    pname4 = StringField('Product Name', validators=[DataRequired()])
    pdescr4 = StringField("Description", validators=[DataRequired()])
    pprice4 = StringField("Price", validators=[DataRequired()])
    quantity4 = StringField('Quantity', validators=[DataRequired()])
    submit4 = SubmitField('Adjust')
    

@bp.route('/sidinventory', methods = ["GET", "POST"])
def sidinventory():
    form = InventoryForm()
    form2 = delete_invForm()
    form3 = add_invForm()
    form4 = change_invForm()
    
    uid = current_user.id
    sid_inventory = Inventory.get_seller(uid)
    
    
    if form.submit.data and form.validate():
        seller_inventory = Inventory.get_seller(form.sid_input.data)
        
        
    if form2.submit2.data and form2.validate():
        Inventory.delete_inventory(uid, form2.pid_input2.data)
        Product.delete_product(form2.pid_input2.data, uid)
        flash("Product Deleted from Inventory. Click 'Refresh Table' to See Change")
        
        
    elif form3.submit3.data and form3.validate():
        pid = Product.get_maxid() +1
        Inventory.add_inventory(uid, pid, form3.productname3.data, form3.quantity3.data)
        Product.add_product(pid, uid, form3.productname3.data, form3.descr.data, form3.cat.data, form3.price.data, True)
        flash("Product Added to Inventory. Click 'Refresh Table' to See Change")

        
    elif form4.submit4.data and form4.validate():
        Inventory.updateQuantity(uid, form4.pid_input4.data, form4.quantity4.data, form4.pname4.data)
        Product.edit_product(form4.pid_input4.data, uid,form4.pname4.data, form4.pdescr4.data, form4.pprice4.data)
        flash("Product Updated. Click 'Refresh Table' to See Change")
        
    
    return render_template('hw4_inventory.html',
                uid = uid,
                sid_inventory = sid_inventory,
                form=form,
                form2=form2,
                form3=form3,
                form4=form4,
                )  
    