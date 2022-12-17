from flask import render_template, request, flash
from flask_login import current_user
from werkzeug.urls import url_parse
import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_login import login_user, logout_user, current_user

from .models.product import Product
from .models.purchase import Purchase
from .models.socials import PReview
from .models.user import User
from .models.carts import Cart
from .models.inventory import Inventory

from flask import Blueprint
bp = Blueprint('product', __name__)

class CartAddForm(FlaskForm):
    quant = StringField('Quantity', validators=[DataRequired()])
    submit = SubmitField("Add to cart.")

@bp.route('/product', methods = ["GET", "POST"])
def product():
    req = request.args
    id = req.get("id")
    product = Product.get(id)

    cat = product.category
    name = product.name
    price = product.price
    avail = product.available
    link = product.link
    descr = product.descr

    cartaddform = CartAddForm()

    uid = Inventory.get_sid(id)
    user = User.get(uid)
    sid = user.id
    sellername = user.firstname + ' ' + user.lastname
    
    products = Product.get_by_cat(cat)[:10]

    if current_user.is_authenticated:
        num_in_cart = Cart.num_items_in_cart(current_user.id)
    else:
        num_in_cart = 0
    
    recentReviews = PReview.getAProductReviews(id)
    recentReviewLinks = PReview.getAPReviewLinks(id)
    
    averageReview = PReview.getAverage(id)
    numberOfReview = PReview.numberOfReview(id)
    numberOfReviewOne = PReview.numberOfReviewOne(id)
    numberOfReviewTwo = PReview.numberOfReviewTwo(id)
    numberOfReviewThree = PReview.numberOfReviewThree(id)
    numberOfReviewFour = PReview.numberOfReviewFour(id)
    numberOfReviewFive = PReview.numberOfReviewFive(id)

    if cartaddform.data and cartaddform.validate():
        Cart.insert_into_cart(current_user.id, id, sid, name, cartaddform.quant.data, price)
        flash("Item has been added to your cart! Go to your cart to view the changes.")
    
    return render_template("product.html", name=name, descr=descr, cat=cat, price=price, avail=avail, link=link, products=products, user = user,
                           pid = id, recentReviews = recentReviews, averageReview = averageReview, numberOfReview = numberOfReview,
                           numberOfReviewOne = numberOfReviewOne, numberOfReviewTwo = numberOfReviewTwo, numberOfReviewThree = numberOfReviewThree,
                           numberOfReviewFour = numberOfReviewFour, numberOfReviewFive = numberOfReviewFive, recentReviewLinks = recentReviewLinks,
                           sellername=sellername, sid=sid, cartaddform=cartaddform, num_in_cart=num_in_cart)
