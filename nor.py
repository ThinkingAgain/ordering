from flask import Flask, render_template, request, send_from_directory
from flask_bootstrap import Bootstrap

#from module import *
from view import *


app = Flask(__name__)
app.secret_key = "thinkagain"
bootstrap = Bootstrap(app)


#db = DBOrding()

@app.route('/')
def index():

    #menu = db.get_today_menu()10
    #menu = {"清蒸鲈鱼":3,"红烧茄子":5, "蒜泥黄瓜":2, "冬瓜炖排骨":8}
    form = TestForm()
    #菜单是一个字典：key=（checkbox的value属性 及 number的name属性）value = label文本
    #这样，当通过menu得到被选择的checkbox时，就可通过checkbox.value=number.name这一关系找到对就的number数量
    menu = {"packed_rice":"米饭盒饭",  "packed_bun": "馒头盒饭"}
    print(menu)

    type1 = '"checkbox"'
    type2 = '"number"'
    return  render_template('ordering.html', menu = menu)

@app.route('/nor', methods=['POST','GET'])
def nor():
    if request.method == 'POST':
        print(request.values)

        for k in request.values.getlist("menu"):
            print(k,request.values.getlist(k)[0])
        form = TestForm()
        return render_template('nor.html',form = form)

#文件下载
@app.route("/down/<filename>")
def download(filename):
    dir = "F:/down"
    return send_from_directory(dir,filename, as_attachment=True)


def main():
    app.run(host='10.74.163.69', port=8801)

if __name__ == "__main__":
    main()


