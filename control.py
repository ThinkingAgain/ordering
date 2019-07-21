from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import RadioField,validators,SelectMultipleField,widgets,TextField, Form

app = Flask(__name__)
app.secret_key ='sdjsldj4323sdsdfssfdf43434'

class MenuForm(FlaskForm):
    radio = RadioField('请选择一个', choices=[('值1', '选项1'), ('值2', '选项2'), ('值3', '选项3')],
                       validators=[validators.AnyOf(['值1', '值2', '值3'], '请选择一个值')])
    selectMultiple = SelectMultipleField('请选择多个选项', choices=[('值1', '选项1'), ('值2', '选项2'), ('值3', '选项3')]
                                         )

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=True)
    option_widget = widgets.CheckboxInput()


class adminForm(Form):
    ip = TextField("订餐人")
    domain_name = TextField('菜单名称')
    domain_ports = MultiCheckboxField('多选', choices=[("a","c"),(2,2)])

@app.route('/publish')
def publish():
    menu = MenuForm()
    menu.radio.choices.append(("选择", "小鸡炖蘑菇"))
    tt = adminForm()


    return render_template("Menu.html", form = menu, tt = tt)