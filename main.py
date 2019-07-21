"""
主页
"""
from flask import Flask, render_template, request, flash
from flask_bootstrap import Bootstrap

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
    if request.method == 'POST':
        if request.form.get("button") == '今日订单':
            today = time.strftime("%Y-%m-%d", time.localtime())
            orders=db.get_orders_list(today)
    return render_template('order_list.html', orders = orders)

#订餐
@app.route('/ordering', methods=['POST','GET'])
def ordering():
    menu = db.get_today_menu()
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



def main():
    app.run(host='0.0.0.0', port=8800)

if __name__ == "__main__":
    main()
