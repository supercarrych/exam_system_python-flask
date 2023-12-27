import pymysql
import requests
from exam import ExamQuestion

db_host = '112.74.47.53'
db_name = 'wechat'
db_user = 'wechat'
db_password = 'ch123456'


class DatabaseHelper:
    def __init__(self):
        self.host = db_host
        self.user = db_user
        self.password = db_password
        self.database = db_name
        self.connection = pymysql.connect(
            host=self.host,
            port=3306,
            user=self.user,
            password=self.password,
            database=self.database,
            charset='utf8mb4'
        )

    def __exit__(self):
        self.connection.__exit__()

    # return cursor object
    def get_cursor(self):
        return self.connection.cursor()

    def get_data(self, table_name, question_id) -> ExamQuestion:
        # query = (
        #     "SELECT image "
        #     "FROM {} WHERE id = %s".format(table_name))
        #
        # cursor = self.connection.cursor(cursor=pymysql.cursors.DictCursor)
        # cursor.execute(query, (question_id,))
        #
        # result = cursor.fetchone()
        # exam = ExamQuestion(question_id, result['image'])
        #
        # cursor.close()
        url = 'http://127.0.0.1:5000/web/api/getImage'
        json = {
            "question_id": question_id,
            "table_name": table_name
        }

        response = requests.post(url=url, json=json)
        res_json = response.json()
        res_json = res_json['data']
        res_json = res_json['result']
        return res_json['image_base_64']

    # 根据id修改题目的question
    def update_question(self, table_name, question_id, question) -> bool:
        try:
            query = ("UPDATE {} SET question = '{}' WHERE id = {}".format(table_name, question, question_id))
            print(query)
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()
            cursor.close()
            return True
        except Exception as e:
            print(e)
            return False

    def disconnect(self):
        if self.connection:
            self.connection.close()

    def getTableName(self):
        sql = 'show tables'
        cursor = self.connection.cursor()
        cursor.execute(sql)
        tableName = cursor.fetchall()
        cursor.close()
        newTableName = []
        for t in tableName:
            newTableName.append(t[0])
        return newTableName

    # get all id from table
    def get_all_id(self, table_name):

        url = 'http://112.74.47.53:5000/api/login'
        json = {
            "open_id": "1231asd"
        }

        response = requests.post(url=url, json=json)

        res_json = response.json()
        print(res_json['data'])
        data = res_json['data']
        auth = str(data['userToken'])

        headers = {
            'Authorization': 'Bearer {}'.format(auth),
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Mobile Safari/537.36'
        }
        url = "http://127.0.0.1:5000/web/api/question/get/{}".format(table_name)
        print(url)
        response = requests.get(url=url, headers=headers)  # 三个参数
        ctx_json = response.json()
        print(ctx_json['data'])
        return ctx_json['data']

    def commit(self):
        return self.connection.commit()  # db.commit()

    def rollback(self):
        return self.connection.rollback()  # db.rollback()
