from flask_wtf import Form,FlaskForm
from wtforms import *
from wtforms.validators import  DataRequired

class TestForm(Form):
    name = StringField("name")
    number = IntegerField("Number:",default=1)
    sub = SubmitField("submit")

class NewMenuForm(FlaskForm):
    name = StringField(u"菜单：", validators=[DataRequired()])
    price = DecimalField(u"价格：", validators=[DataRequired()])
    sub = SubmitField(u"增加菜单")