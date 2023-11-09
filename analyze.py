import re
from itertools import zip_longest
from DB import DatabaseHelper

import pymysql

from exam import ExamQuestion

table_name = 'question'


class ExamHelper:

    def __init__(self):
        self.db = DatabaseHelper()
        self.cursor = self.db.get_cursor()
        self.initExam()
        self.question_id = []

    def initExam(self):
        self.question_id = self.db.get_all_id(table_name)


    def getData(self, table_name, question_id):
        query = (("SELECT question, solution FROM {} WHERE id = %s").format(table_name))

        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(query, (question_id,))

    def analyze(self):
        lists = []
        for i in self.question_id:
            exam = self.db.get_data(table_name, i)
            lists.append({'question': exam.question, 'items': exam.options})

        return lists

    def decidetra(self, a):
        if a == '×':
            return 0
        elif a == '√':
            return 1
        else:
            return a

    # def makepaper(self):
    #     for index, item in enumerate(analyze()):
    #         answer = list(map(decidetra, getAnswer()))[index]
    #         sql = 'select count(*) as last_id from docx'
    #         cursor.execute(sql)
    #         paper_id = cursor.fetchone().get('last_id')
    #
    #         sql = 'insert into questions (q_text,q_type,q_value,A,B,C,D,paper_id,answer) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    #
    #         if index <= 23:
    #             cursor.execute(sql, (
    #                 item.get('question'), 'radio', 1.5, item.get('items')[0], item.get('items')[1],
    #                 item.get('items')[2],
    #                 item.get('items')[3], paper_id, answer))
    #
    #             db.commit()
    #
    #         if index > 23 and index < 36:
    #             cursor.execute(sql, (
    #                 item.get('question'), 'checkbox', 2, item.get('items')[0], item.get('items')[1],
    #                 item.get('items')[2],
    #                 item.get('items')[3], paper_id, answer))
    #
    #             db.commit()
    #
    #         if index >= 36:
    #             cursor.execute(sql, (
    #                 item.get('question'), 'decide', 1, '1', 0, 0,
    #                 0, paper_id, answer))
    #
    #             db.commit()

# if __name__ == '__main__':
#     initDocx('stefan', 'e:/test.docx')
