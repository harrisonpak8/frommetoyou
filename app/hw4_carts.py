from flask import render_template, request, session
from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import ValidationError, DataRequired, NumberRange
from .models.carts import Cart
from .models.user import User

from flask import Blueprint
bp = Blueprint('hw4_carts', __name__)

class DeleteFromCartForm(FlaskForm):
    pid_input = StringField('Product ID', validators=[DataRequired()])
    submit = SubmitField('Delete') 

class ChangeItemQuantity(FlaskForm):
    pid_input = StringField('Product ID', validators=[DataRequired()])
    quant_input = StringField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Update Quantity')

@bp.route('/uidcart', methods = ["GET", "POST"])
def uidcart():
    if current_user.is_authenticated:
        uid = current_user.id
        balance = User.current_ubalance(uid)

        cart = Cart.get_cart(uid)

        subtotal = Cart.subtotal(uid)

        num_in_cart = Cart.num_items_in_cart(uid)
        
        deleteform = DeleteFromCartForm()
        changeform = ChangeItemQuantity()
        
        if deleteform.submit.data and deleteform.validate():
            Cart.delete_cart_item(uid, deleteform.pid_input.data)
        
        #elif changeform.submit.data and changeform.validate():
         #   Cart.update_quantity(uid, changeform.pid_input.data, changeform.quant_input.data)
        

        return render_template('hw4_carts.html',
                                deleteform=deleteform,
                                changeform=changeform,
                                cart=Cart.get_cart(uid),
                                num_in_cart=Cart.num_items_in_cart(uid),
                                subtotal=Cart.subtotal(uid),
                                balance=balance
                              ) 
    else:
        return render_template('hw4_carts.html')

    
    # render the page by adding information to the index.html file
    

