from flask_wtf import Form
from wtforms import *
from wtforms.validators import  DataRequired

class TestForm(Form):
    name = StringField("name")
    number = IntegerField("Number:",default=1)
    sub = SubmitField("submit")