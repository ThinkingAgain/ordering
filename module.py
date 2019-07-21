import pymysql
import time

class DBOrdering:
    """MySql--DB："""
    DB = "todo"
    PW = "asdfwj"
    #每日菜单 {id:{显示文本，价格}}
    DAILY_MENU = {"packed_rice": {"label":"米饭盒饭","price":8},
                  "packed_bun":{"label": "馒头盒饭","price":8},
                  "rice": {"label":"米饭","price":1},
                  "bun":{"label": "馒头","price":1},
                  "muslim_packed_rice":{"label": "清真米饭盒饭","price":8},
                  "muslim_packed_bun":{"label": "清真馒头盒饭","price":8}

                  }

    def get_conn(self):
        '''连接数据库'''
        try:
            self.conn = pymysql.connect(host='127.0.0.1',user='root',
                                        passwd=DBOrdering.PW,port=3306,
                                        charset='utf8',db=DBOrdering.DB)
        except pymysql.Error as e:
            print(e)
            print('数据库连接失败')

    def close_conn(self):
        '''关闭数据库'''
        try:
            if self.conn:
                self.conn.close()
        except pymysql.Error as e:
            print(e)
            print('关闭数据库失败')

    def _change_db(self, sql_list):
        '''使用sql语句列表操作（IUD）数据库:成功返回1，失败回滚并返回0'''
        try:
            self.get_conn()
            cursor = self.conn.cursor()
            for sql in sql_list:
                #print(sql)
                cursor.execute(sql)
            # 一定需要提交事务，要不不会显示，只会占位在数据库
            self.conn.commit()
            return 1
        except AttributeError as e:
            print('Error:', e)
            return 0
        except TypeError as e:
            print('Error:', e)
            # 发生错误还提交就是把执行正确的语句提交上去
            # self.conn.commit()
            # 下面这个方法是发生异常就全部不能提交,但语句执行成功的就会占位
            self.conn.rollback()
            return 0
        finally:
            cursor.close()
            self.close_conn()

    def get_all(self, sql):
        '''
        返回sql语句查询到的所有数据。
        返回值：嵌套元组
        '''
        self.get_conn()
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            return cursor.fetchall()

        except AttributeError as e:
            print(e)
            return None
        finally:
            self.close_conn()


    def old_get_today_menu(self):
        '''查询今日菜单'''
        today = time.strftime("%Y-%m-%d",time.localtime())
        sql = 'SELECT course,cost FROM `menu` WHERE pub_date = "{}"'.format(today)
        menu = self.get_all(sql)

        #将数据转为字典并返回
        return dict(menu)

    def get_today_menu(self):
        '''返回今日菜单（dict）'''
        # 菜单是一个字典：key=（checkbox的value属性 及 number的name属性）value = label文本
        # 这样，当通过menu得到被选择的checkbox时，就可通过checkbox.value=number.name这一关系找到对就的number数量
        menu = DBOrdering.DAILY_MENU
        return menu

    def get_custom(self):
        '''返回订餐人名单（列表）'''
        sql =  'SELECT custom FROM `customs`; '
        # 利用列表推导将数据转为列表并返回
        return [x[0] for x in self.get_all(sql)]

    def get_orders_list(self,date_string):
        sql = "SELECT id,order_date,orders.custom,content,cost,customs.account FROM " \
              "orders LEFT JOIN customs ON orders.custom=customs.custom " \
              "WHERE order_date='{}'ORDER BY orders.custom;".format(date_string)
        return [list(x) for x in self.get_all(sql)]

    def append_orders(self, order_dict, custom_list, today_menu_dict):
        '''订单入库：orders
        *menu_dict: 订餐内容字典{菜：数量}
        *custom_list:订餐人列表
        *today_menu_dict:今日菜单
        '''
        content = "" #订餐内容
        cost = 0    #价格
        for k, v in order_dict.items():
            content += today_menu_dict[k]["label"]+":"+v+","
            if k in DBOrdering.DAILY_MENU:
                cost += today_menu_dict[k]["price"] * int(v)
            else:
                print("Error:", k,"不在菜单中")

        today = time.strftime("%Y-%m-%d", time.localtime())
        sql_list = []
        for custom in custom_list:
            sql_list.append("INSERT INTO orders(custom,content,cost,order_date) " \
                  "VALUES('{}','{}',{},'{}');".format(custom,content[:-1],cost,today))
        #将更新订餐人余额语句追加至sql列表
        sql_list.extend(self._get_sqllistOf_updateCustomAccount(custom_list, cost))

        return self._change_db(sql_list)

    def _get_sqllistOf_updateCustomAccount(self, custom_list, cost):
        """生成sql语句列表实现：订餐人账户余额-cost花销"""
        # 获得订餐人-账户余额(字典)
        custom_sql = "SELECT * FROM customs WHERE custom in ('{}');".format("','".join(custom_list))
        custom_account = dict(self.get_all(custom_sql))
        # 订餐人-帐户余额（字典）扣除订单金额
        for x in custom_list:
            custom_account[x] -= cost
        # 生成更新订餐人账户的sql列表
        sqllist = []
        for custom, account in custom_account.items():
            sqllist.append("UPDATE customs SET account={} WHERE custom='{}';".format(account, custom))

        return sqllist







if __name__ == '__main__':
    db = DBOrdering()
    print(db.get_orders_list('2019-7-18'))
    #order_dict = {"packed_rice": "2","rice": "3"}
    #print(db.append_orders(order_dict,["李杰","张磊","王刚"], db.DAILY_MENU))
    #sql = ["INSERT INTO orders(custom,content,cost,order_date) VALUES('李杰','packed_rice:2,rice:3',40,'2019-07-18');"]
    #print(db.insert_db(sql))




