import pymysql

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

    # return cursor object
    def get_cursor(self):
        return self.connection.cursor()

    def get_data(self, table_name, question_id) -> ExamQuestion:
        query = (
            "SELECT type_desc,question,options,solution,analysis,paper_name,paper_bonus,nth,issues_count,my_solution "
            "FROM {} WHERE id = %s".format(table_name))

        cursor = self.connection.cursor(cursor=pymysql.cursors.DictCursor)
        cursor.execute(query, (question_id,))

        result = cursor.fetchone()
        exam = ExamQuestion(
            question_id, result['type_desc'], result['question'], result['options'], result['solution'],
            result['analysis'], result['paper_name'], result['paper_bonus'], result['nth'],
            result['issues_count'], result['my_solution']
        )

        cursor.close()

        return exam

    def disconnect(self):
        if self.connection:
            self.connection.close()

    # get all id from table
    def get_all_id(self, table_name):
        query = (("SELECT id FROM {}").format(table_name))

        cursor = self.connection.cursor()
        cursor.execute(query)

        result = cursor.fetchall()
        cursor.close()

        return result

    # db = pymysql.connect(
    #     host='112.74.47.53',
    #     port=3306,
    #     db='db_exam',
    #     user='db_exam',
    #     password='ch5023429',
    #     charset='utf8mb4'
    # )
    # db2 = pymysql.connect(
    #     host='112.74.47.53',
    #     port=3306,
    #     db='wechat',
    #     user='wechat',
    #     password='ch123456',
    #     charset='utf8mb4'
    # )
    #
    # cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    # cursor_exam = db2.cursor(cursor=pymysql.cursors.DictCursor)
    def commit(self):
        return self.connection.commit()    # db.commit()

    def rollback(self):
        return self.connection.rollback()    # db.rollback()

