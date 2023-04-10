import requests
import pymysql
api_url = 'https://api.github.com/search/repositories?q=spider'
req = requests.get(api_url)
print('状态码：',req.status_code)
req_dic = req.json()
print('与spider有关的库总数：',req_dic['total_count'])
print('本次请求是否完整:',req_dic['incomplete_results'])
req_dic_items = req_dic['items']
print('当前页面返回的项目数量：',len(req_dic_items))
names = []

for key in req_dic_items:
    names.append(key['name'])

sorted_names = sorted(names)

db = pymysql.connect(host='localhost', user='root', password='这里要使用自己密码', port=3306)
cursor = db.cursor()
cursor.execute("CREATE DATABASE 数据库名称 DEFAULT CHARACTER SET utf8mb4")
db.close()

db2 = pymysql.connect("localhost", "root", "这里要使用自己密码", "数据库名称",3306)
cursor2 = db2.cursor()
cursor2.execute("DROP TABLE IF EXISTS 数据库名称")
sql1 = """CREATE TABLE `数据库名称`(
              `id` int(10) NOT NULL AUTO_INCREMENT,
              `full_name` char(20) NOT NULL,
               PRIMARY KEY (`id`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"""
cursor2.execute(sql1)
print("Created table Successfull.")

for index,name in enumerate(sorted_names):
    print('项目索引号：',index,'  项目名称：',name)

    sql2 = 'INSERT INTO 数据库名称(id, full_name) VALUES(%s,%s)'
    try:
        cursor2.execute(sql2, (index, name))
        db2.commit()
    except:
        db2.rollback()
db2.close()

