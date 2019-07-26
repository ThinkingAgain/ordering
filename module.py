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
            print("异常：",e)
            return None
        finally:
            self.close_conn()


    def old_get_today_menu(self):
        '''（已废弃）查询今日菜单'''
        today = time.strftime("%Y-%m-%d",time.localtime())
        sql = 'SELECT course,cost FROM `menu` WHERE pub_date = "{}"'.format(today)
        menu = self.get_all(sql)

        #将数据转为字典并返回
        return dict(menu)

    def insert_specail_menu(self,special_menu_name, special_menu_price):
        """新增特别菜单，如存在则更新"""
        today = time.strftime("%Y-%m-%d", time.localtime())
        sql = "SELECT * FROM menu WHERE course = '{}';".format(special_menu_name)
        if self.get_all(sql):
            sql = "UPDATE menu SET pub_date='{}',cost={} WHERE course = '{}';".format(today, special_menu_price, special_menu_name)
        else:
            sql = "INSERT INTO menu VALUES ('{}','{}',{});".format(today, special_menu_name, special_menu_price)

        return self._change_db([sql])


    def update_special_menu(self, special_menu_list):
        """将special_menu_list中的菜单项在menu表中更新
        为当日日期
        """
        today = time.strftime("%Y-%m-%d", time.localtime())
        sql_list = []
        for course in special_menu_list:
            sql_list.append("UPDATE menu SET pub_date = '{}' WHERE course = '{}';".format(today, course))
        return self._change_db(sql_list)

    def get_special_menu(self):
        '''在menu表中查询当日菜单（周四包子）
        返回DAILY_MENU结构的嵌套字典
        '''
        #不是周四就返回空字典
        if time.strftime("%w", time.localtime()) != "4" :
            return {}
        #周四返回菜单字典
        today = time.strftime("%Y-%m-%d", time.localtime())
        sql = 'SELECT course,cost FROM `menu`;'# WHERE pub_date = "{}"'.format(today)
        menu = self.get_all(sql)

        # 将数据转为DAILY_MENU型字典并返回
        menu_dict = {}
        for item in menu:
            temp = {"label":item[0],"price":item[1]}
            menu_dict[item[0]] = temp
        return menu_dict


    def get_today_menu(self):
        '''返回今日菜单（dict）'''
        # 菜单是一个字典：key=（checkbox的value属性 及 number的name属性）value = label文本
        # 这样，当通过menu得到被选择的checkbox时，就可通过checkbox.value=number.name这一关系找到对就的number数量
        if time.strftime("%w", time.localtime()) != "4" :
            return DBOrdering.DAILY_MENU
        #周四返回菜单字典
        today = time.strftime("%Y-%m-%d", time.localtime())
        sql = 'SELECT course,cost FROM `menu` WHERE pub_date = "{}"'.format(today)
        menu = self.get_all(sql)

        # 将数据转为DAILY_MENU型字典并返回
        menu_dict = {}
        for item in menu:
            temp = {"label":item[0],"price":item[1]}
            menu_dict[item[0]] = temp

        return menu_dict

    def get_custom(self):
        '''返回订餐人名单（列表）'''
        sql =  'SELECT custom FROM `customs`; '
        # 利用列表推导将数据转为列表并返回
        return [x[0] for x in self.get_all(sql)]

    def get_orders_list(self,date_string):
        """返回订单嵌套列表(日期字符串）
        【【id,日期，订餐人，订单内容，价格，订餐人账户余额】，【。。。】，。。。】
        """
        sql = "SELECT id,order_date,orders.custom,content,cost,customs.account FROM " \
              "orders LEFT JOIN customs ON orders.custom=customs.custom " \
              "WHERE order_date='{}'ORDER BY orders.custom;".format(date_string)
        return [list(x) for x in self.get_all(sql)]

    def get_summary_of_orders(self, orders:list)->dict:
        """返回订单列表的汇总情况（orders:嵌套列表）
        返回字典{菜单：数量，。。。}
        """
        summary = {}
        for order in orders:
            for items in order[3].split(","): #下标3为订餐内容
                item = items.split(":")
                if item[0] in summary:
                    summary[item[0]] += int(item[1])
                else:
                    summary[item[0]] = 1

        return summary

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
            if k in today_menu_dict:
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
    print(type(time.strftime("%w", time.localtime())))
    print(db.get_special_menu())
    #order = [[0,1,1,"米饭:1,馒头:2"],[0,1,1,"大米饭:1,馒头:2"]]
    #print(db.get_summary_of_orders(order))
    #print(db.get_orders_list('2019-7-19'))
    #order_dict = {"packed_rice": "2","rice": "3"}
    #print(db.append_orders(order_dict,["李杰","张磊","王刚"], db.DAILY_MENU))
    #sql = ["INSERT INTO orders(custom,content,cost,order_date) VALUES('李杰','packed_rice:2,rice:3',40,'2019-07-18');"]
    #print(db.insert_db(sql))




