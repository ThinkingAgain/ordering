import pymysql
# 连接数据库


try:
  db = pymysql.connect(host='127.0.0.1',user='root',passwd='asdfwj',db='todo',port=3306,charset='utf8') 
  # 检验数据库是否连接成功 
  cursor = db.cursor() 
  # 这个是执行sql语句，返回的是影响的条数 
  data = cursor.execute('SELECT * FROM `menu`') 
  # 得到一条数据 
  one = cursor.fetchone() 
  print(data)
  print(one)
except pymysql.Error as e:
  print(e)
  print('操作数据库失败')
finally:
  # 如果连接成功就要关闭数据库
  if db:
	db.close()
	
	
	
# 将一条数据转成字典方便查找
new = dict(zip([x[0] for x in cursor.description],[x for x in cursor.fetchone()]))
print(new)


#将多条数据转为字典
def new2dict(new):
	return dict(zip([x[0] for x in cursor.description],[x for x in new]))
news_list = list(map(new2dict,cursor.fetchall()))


#面向对象的示例（问题是会产生过多的数据库连接）
import pymysql 
class MysqlSearch(object):
 
	 def get_conn(self): 
	 '''连接mysql数据库''' 
		 try: 
			self.conn = pymysql.connect(host='127.0.0.1',user='root',passwd='your password',port=3306,charset='utf8',db='news') 
		 except pymysql.Error as e: 
			 print(e) 
			 print('连接数据库失败')

	 def close_conn(self):
	 '''关闭数据库'''
		 try:
			 if self.conn:
				self.conn.close()
		 except pymysql.Error as e:
			 print(e)
			 print('关闭数据库失败')

	 def get_one(self):
	 '''查询一条数据'''
		try:
			 # 这个是连接数据库
			 self.get_conn()
			 # 查询语句
			 sql = 'SELECT * FROM `new` WHERE `type`=%s'
			 # 这个光标用来执行sql语句
			 cursor = self.conn.cursor()
			 cursor.execute(sql,('英超',))
			 new = cursor.fetchone()
			 # 返回一个字典，让用户可以按数据类型来获取数据
			 new_dict = dict(zip([x[0] for x in cursor.description],new))
			 # 关闭cursor
			 cursor.close()
			self.close_conn()
			 return new_dict
		 except AttributeError as e:
			 print(e)
			 return None
	
	def get_all(self):
		'''获取所有结果'''
		sql = 'SELECT * FROM `new` '
		self.get_conn()
		try:
			cursor = self.conn.cursor()
			cursor.execute(sql)
			news = cursor.fetchall()
			# 将数据转为字典，让用户根据键来查数据
			news_list =list(map(lambda x:dict(zip([x[0] for x in cursor.description],[d for d in x])),news))
			# 这样也行,连续用两个列表生成式
			news_list = [dict(zip([x[0] for x in cursor.description],row)) for row in news]
			cursor.close()
			self.close_conn()
			return news_list
		except AttributeError as e:
			print(e)
			return None

def main():
	 # 获取一条数据
	 news = MysqlSearch()
	 new = news.get_one()
	 if new:
		print(new)
	 else:
		print('操作失败')

	 # 获取多条数据
	 news = MysqlSearch()
	 rest = news.get_all()
	 if rest:
		 print(rest)
		 print(rest[7]['type'],rest[7]['title'])
		 print('类型：{0},标题：{1}'.format(rest[12]['type'],rest[12]['title']))
		 for row in rest:
			print(row)
	 else:
		print('没有获取到数据')

if __name__ == '__main__':
 main()
 
 
 
 
 #根据页数来进行查询指定的数据数
 def get_more(self,page,page_size): 
	 '''查多少页的多少条数据''' 
	 offset = (page-1)*page_size 
	 sql = 'SELECT * FROM `new` LIMIT %s,%s' 
	 try: 
		 self.get_conn() 
		 cursor = self.conn.cursor() 
		 cursor.execute(sql,(offset,page_size,)) 
		 news = [dict(zip([x[0] for x in cursor.description],new)) for new in cursor.fetchall()]
		  cursor.close()
		  self.close_conn()
		  return news
	  except AttributeError as e:
		  print(e)
		  return None
	  
def main():
	  #获取某页的数据
	  news = MysqlSearch()
	  new = news.get_more(3,5)
	  if new:
		  for row in new:
			print(row)
	  else:
		print('获取数据失败')
 
 if __name__ == '__main__':
  main()
  



#增加数据到数据库 
#需要提交事务，这就需要用到cursor.commit()来进行提交，在增加数据后，如果不提交，数据库就不会显示 
def add_one(self): 
	sql = 'INSERT INTO `new`(`title`,`content`,`type`,`view_count`,`release_time`) VALUE(%s,%s,%s,%s,%s)' 
	try: 
		self.get_conn() 
		cursor = self.conn.cursor() 
		cursor.execute(sql, ('title', 'content', 'type', '1111', '2018-02-01')) 
		cursor.execute(sql, ('标题', '内容', '类型', '0000', '2018-02-01')) 
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

def main():
	news = OperateSQL()
	if news.add_one():
		print('增加数据成功')
	else:
		print('发生异常，请检查！！！')

if __name__ == '__main__':
	main()