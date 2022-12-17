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
bp = Blueprint('sellerreview', __name__)

UPLOAD_FOLDER = '/uploads/'

class createForm(FlaskForm):
    ratingInCreate = SelectField('Rating', choices=['1','2','3','4','5'], validators=[DataRequired()])
    reviewInCreate = StringField('Review', validators=[DataRequired()])
    submitCreate = SubmitField('Submit')
    
class updateForm(FlaskForm):
    ratingInUpdate = SelectField('Rating', choices=['1','2','3','4','5'], validators=[DataRequired()])
    reviewInUpdate = StringField('Review')
    submitUpdate = SubmitField('Update')    

class deleteForm(FlaskForm):
    submitDelete = SubmitField('Delete')

@bp.route('/sellerreview', methods = ["GET", "POST"])
def sellerreview():
    cForm = createForm()
    uForm = updateForm()
    dForm = deleteForm()
    
    req = request.args
    sid = req.get("sid")
    name = req.get("name")
    uid = current_user.id
    
    orderExist = PReview.sellerOrderExist(uid, sid)
    reviewExist = PReview.sellerReviewexist(uid, sid)
    
    
    if cForm.submitCreate.data and cForm.validate():
        PReview.createSellerReview(uid, sid, cForm.ratingInCreate.data, cForm.reviewInCreate.data)
        flash('You have successfully added a review for this product!')
            
    elif uForm.submitUpdate.data and uForm.validate():
        PReview.updateSellerReview(uid, sid, uForm.ratingInUpdate.data, uForm.reviewInUpdate.data)
        flash('You have successfully updated a review for this product!')
        
    elif dForm.submitDelete.data and dForm.validate():
        PReview.deleteSellerReview(uid, sid)
        flash('You have successfully deleted a review for this product!')
        
   
    return render_template("sellerreview.html",sid = sid, uid = uid, orderExist = orderExist, reviewExist = reviewExist, name = name, cForm = cForm, uForm = uForm, dForm = dForm)