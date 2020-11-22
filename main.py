"""
主页
"""
from flask import Flask, render_template, request, flash
from flask_bootstrap import Bootstrap
import  decimal

from module import *
from view import *

app = Flask(__name__)
app.secret_key = "thinkagain" #跨域访问
bootstrap = Bootstrap(app)

db = DBOrdering()

@app.route('/')
def index():
    #menu = db.get_today_menu()
    return  render_template('Main.html')

#订单查询
@app.route('/order_list', methods=['POST','GET'])
def order_list():
    orders = []
    total_cost = 0
    summary_of_orders = {}
    if request.method == 'POST':
        if request.form.get("button") == '今日订单':
            today = time.strftime("%Y-%m-%d", time.localtime())
            orders=db.get_orders_list(today)
            #统计全部订单价格
            for order in orders:
                total_cost += order[4] #下标4为cost的存储位置，也许用字典更好
            #统计订单汇总数据
            summary_of_orders = db.get_summary_of_orders(orders)
    return render_template('order_list.html', orders = orders, total_cost=total_cost,
                           summary_of_orders=summary_of_orders)

#订餐
@app.route('/ordering', methods=['POST','GET'])
def ordering():
    menu = db.get_today_menu()
    if not menu:
        flash("今日周四！需发布菜单后方可点餐！", "error")
    if request.method == 'POST':
        order_dict={} #订餐清单
        for course in request.values.getlist("menu"):
            #flash("{}: {}".format(course, request.values.getlist(course)[0]))
            order_dict[course] = request.values.getlist(course)[0]

        custom_list =[] #订餐人清单
        for name in request.values.getlist("custom"):
            #flash("订餐人: {}".format(name))
            custom_list.append(name)
        if order_dict and custom_list:
            if(db.append_orders(order_dict, custom_list, menu)):
                flash("、".join(custom_list)+"订餐成功!")
            else:
                flash("订餐失败！")
        else:
            flash("请勾选订餐人和菜单后再提交！")

    custom = db.get_custom()
    return render_template('ordering.html', menu=menu, custom=custom)

#发布菜单
@app.route('/publish_menu', methods=['POST','GET'])
def publish_menu():
    new_menu_form = NewMenuForm()
    if request.method == 'POST' and request.form.get("sub") == "发布周四菜单":
        special_menu_list = []
        for course in request.values.getlist("menu"):
            special_menu_list.append(course)
        db.update_special_menu(special_menu_list)
        if special_menu_list:
            flash("、".join(special_menu_list)+" 已发布至今日菜单")

    if request.method == 'POST' and new_menu_form.validate_on_submit():
       db.insert_specail_menu(new_menu_form.name.data, new_menu_form.price.data)
       flash("新增菜单成功！")
       new_menu_form.name.process_data("")
       new_menu_form.price.raw_data = "0.0"


    menu = db.get_special_menu()
    return render_template('publish_menu.html', menu=menu, new_menu_form=new_menu_form)



def main():
    app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    main()
