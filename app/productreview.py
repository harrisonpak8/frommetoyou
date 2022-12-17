import os
from flask import Flask, render_template, request, flash, redirect
from flask_login import current_user
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
import datetime
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, FileField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
import subprocess

from .models.product import Product
from .models.purchase import Purchase
from .models.socials import PReview
from .models.user import User

from flask import Blueprint
bp = Blueprint('productreview', __name__)


class createForm(FlaskForm):
    ratingInCreate = SelectField('Rating', choices=['1','2','3','4','5'], validators=[DataRequired()])
    reviewInCreate = StringField('Review', validators=[DataRequired()])
    photoInCreate = StringField('Product Photo (use link)', validators=[DataRequired()])
    submitCreate = SubmitField('Submit')
    
class updateForm(FlaskForm):
    ratingInUpdate = SelectField('Rating', choices=['1','2','3','4','5'], validators=[DataRequired()])
    reviewInUpdate = StringField('Review')
    photoInUpdate = StringField('Product Photo (use link)', validators=[DataRequired()])
    submitUpdate = SubmitField('Update')    

class deleteForm(FlaskForm):
    submitDelete = SubmitField('Delete')

@bp.route('/productreview', methods = ["GET", "POST"])
def productreview():
    cForm = createForm()
    uForm = updateForm()
    dForm = deleteForm()
    
    req = request.args
    pid = req.get("pid")
    name = req.get("name")
    link = req.get("link")
    uid = req.get("uid")
    cat= req.get("cat")
    price = req.get("price")
    avail = req.get("avail")
    
    orderExist = PReview.orderExist(uid, pid)
    reviewExist = PReview.reviewexist(uid, pid)
    
    
    if cForm.submitCreate.data and cForm.validate():
        PReview.createProductReview(uid, pid, cForm.ratingInCreate.data, cForm.reviewInCreate.data, cForm.photoInCreate.data)
        flash('You have successfully added a review for this product!')
            
    elif uForm.submitUpdate.data and uForm.validate():
        PReview.updateProductReview(uid, pid, uForm.ratingInUpdate.data, uForm.reviewInUpdate.data, uForm.photoInUpdate.data)
        flash('You have successfully updated a review for this product!')
        
    elif dForm.submitDelete.data and dForm.validate():
        PReview.deletereview(uid, pid)
        flash('You have successfully deleted a review for this product!')
        
   
    return render_template("productreviews.html", pid=pid,  uid = uid, name = name, link = link, cat = cat, price = price, avail = avail, orderExist = orderExist, reviewExist = reviewExist, cForm = cForm, uForm = uForm, dForm = dForm)