数据类型：
菜单字典：{name:{"label":label(~可与name相同~),"price":价格}，}
DAILY_MENU={"packed_rice": {"label":"米饭盒饭","price":8},
                  "packed_bun":{"label": "馒头盒饭","price":8},
                  "rice": {"label":"米饭","price":1},
                  "bun":{"label": "馒头","price":1},
                  "muslim_packed_rice":{"label": "清真米饭盒饭","price":8},
                  "muslim_packed_bun":{"label": "清真馒头盒饭","price":8}

                  }

数据库表结构
CREATE TABLE menu(
pub_date date Not NULL,
course varchar(20) PRIMARY KEY UNIQUE, 
cost DECIMAL(10,2) NOT NULL
);

INSERT INTO menu VALUES('2019-7-14','烧茄子',6);
INSERT INTO menu VALUES('2019-7-14',"番茄炒蛋",6), ('2019-7-10',"冬瓜炖排骨",15),( '2019-7-14',"小鸡炖蘑菇",10);

UPDATE menu SET pub_date = '2019-7-24' WHERE course = '烧茄子';

UPDATE menu SET pub_date = '2019-7-15' WHERE course = "番茄炒蛋" OR course = "冬瓜炖排骨";

订单(订单号 订餐人 订单内容 价格 日期 备注）-----------------------
CREATE TABLE orders(
id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
custom varchar(10) NOT NULL,
content varchar(30) NOT NULL,
cost DECIMAL(10,2) NOT NULL, 
order_date date Not NULL,
memo varchar(50)
);
INSERT INTO orders(custom,content,cost,order_date) VALUES('张三','烧茄子:1,米饭:2',10,'2019-7-18');


INSERT INTO orders(custom,content,cost,order_date) VALUES(李杰,packed_rice:2,rice:3,,40,2019-07-18);
INSERT INTO orders(custom,content,cost,order_date) VALUES(张磊,packed_rice:2,rice:3,,40,2019-07-18);
 INSERT INTO orders(custom,content,cost,order_date) VALUES(王刚,packed_rice:2,rice:3,,40,2019-07-18);
 
 
订餐人员账户（订餐人 账户余额）
CREATE TABLE customs(
custom varchar(10) NOT NULL PRIMARY KEY UNIQUE,
account DECIMAL(10,2) NOT NULL DEFAULT 0
);
INSERT INTO customs(custom) VALUES ('李杰');
INSERT INTO customs VALUES ('张磊',100),('王刚',100);
INSERT INTO customs VALUES ('周艳',100),('郑平',100),('曹明',100);

SELECT * FROM customs WHERE custom in ('周艳','郑平','曹明');
SELECT id,custom,content,cost FROM orders WHERE order_date='{}';
UPDATE customs SET account=80 WHERE custom='李杰';

UPDATE orders SET cost=8.8 WHERE id=43;

SELECT id,oder_date,orders.custom,content,cost,customs.account FROM orders LEFT JOIN customs ON orders.custom=customs.custom WHERE order_date='2019-7-18';
