import os
from flask import Flask, render_template, request, flash, redirect, session
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

class messagingForm(FlaskForm):
    message = StringField('Message', validators=[DataRequired()])
    submit = SubmitField('Send') 

from flask import Blueprint
bp = Blueprint('messaging', __name__)

@bp.route('/convo', methods = ["GET", "POST"])
def convo():
    
    id = current_user.id
    if session['seller'] == False:
        conversations = PReview.getUserConvo(id)
    else:
        conversations = PReview.getSellerConvo(id)    
   
    return render_template("conversations.html", conversations = conversations)

@bp.route('/mdisplay', methods = ["GET", "POST"])
def mdisplay():
    req = request.args
    cid = req.get("cid")
    id = req.get("id")
    
    form = messagingForm()
    
    messages = PReview.getMessages(cid)
    
    if form.submit.data and form.validate():
        PReview.addMessage(cid, id, form.message.data)
        flash("Message Sent!, Refresh to Update")
      
   
    return render_template("mdisplay.html", messages = messages, form = form)