�������ͣ�
�˵��ֵ䣺{name:{"label":label(~����name��ͬ~),"price":�۸�}��}
DAILY_MENU={"packed_rice": {"label":"�׷��з�","price":8},
                  "packed_bun":{"label": "��ͷ�з�","price":8},
                  "rice": {"label":"�׷�","price":1},
                  "bun":{"label": "��ͷ","price":1},
                  "muslim_packed_rice":{"label": "�����׷��з�","price":8},
                  "muslim_packed_bun":{"label": "������ͷ�з�","price":8}

                  }

���ݿ��ṹ
CREATE TABLE menu(
pub_date date Not NULL,
course varchar(20) PRIMARY KEY UNIQUE, 
cost DECIMAL(10,2) NOT NULL
);

INSERT INTO menu VALUES('2019-7-14','������',6);
INSERT INTO menu VALUES('2019-7-14',"���ѳ���",6), ('2019-7-10',"�������Ź�",15),( '2019-7-14',"С����Ģ��",10);

UPDATE menu SET pub_date = '2019-7-24' WHERE course = '������';

UPDATE menu SET pub_date = '2019-7-15' WHERE course = "���ѳ���" OR course = "�������Ź�";

����(������ ������ �������� �۸� ���� ��ע��-----------------------
CREATE TABLE orders(
id int NOT NULL PRIMARY KEY AUTO_INCREMENT,
custom varchar(10) NOT NULL,
content varchar(30) NOT NULL,
cost DECIMAL(10,2) NOT NULL, 
order_date date Not NULL,
memo varchar(50)
);
INSERT INTO orders(custom,content,cost,order_date) VALUES('����','������:1,�׷�:2',10,'2019-7-18');


INSERT INTO orders(custom,content,cost,order_date) VALUES(���,packed_rice:2,rice:3,,40,2019-07-18);
INSERT INTO orders(custom,content,cost,order_date) VALUES(����,packed_rice:2,rice:3,,40,2019-07-18);
 INSERT INTO orders(custom,content,cost,order_date) VALUES(����,packed_rice:2,rice:3,,40,2019-07-18);
 
 
������Ա�˻��������� �˻���
CREATE TABLE customs(
custom varchar(10) NOT NULL PRIMARY KEY UNIQUE,
account DECIMAL(10,2) NOT NULL DEFAULT 0
);
INSERT INTO customs(custom) VALUES ('���');
INSERT INTO customs VALUES ('����',100),('����',100);
INSERT INTO customs VALUES ('����',100),('֣ƽ',100),('����',100);

SELECT * FROM customs WHERE custom in ('����','֣ƽ','����');
SELECT id,custom,content,cost FROM orders WHERE order_date='{}';
UPDATE customs SET account=80 WHERE custom='���';

UPDATE orders SET cost=8.8 WHERE id=43;

SELECT id,oder_date,orders.custom,content,cost,customs.account FROM orders LEFT JOIN customs ON orders.custom=customs.custom WHERE order_date='2019-7-18';
