import json
import os
import random
from datetime import timedelta

from flask import Flask, render_template, request, jsonify, session
# from flask_uploads import configure_uploads, UploadSet

from flask_cors import CORS
from DB import DatabaseHelper
from analyze import ExamHelper

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['SECRET_KEY'] = os.urandom(24)
paper_id = ''
user_name = ''
db = DatabaseHelper()
cursor = db.get_cursor()

# app.config['UPLOADS_DEFAULT_DEST'] = 'D:/'  # 这里指定的是 DEFAULT 这个集合里面类型的文件 存放在什么地方
# app.config['UPLOADS_DEFAULT_URL'] = 'http://127.0.0.1/uploadfile/'
# fileSet = UploadSet('docx', )  # 这里指定的是文件夹  D:/file/     extensions=IMAGES 这个参数可以限制上传文件类型，可以从源码里面看
# configure_uploads(app, fileSet)  # 这里是让配置生效


@app.route('/')
def index():

    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return 'GET'
    else:
        email = request.form['email']
        password = request.form['password']

        sql = "select id,realname from users where email=%s and password=%s"
        res = cursor.execute(sql, (email, password))

        if res:
            result = cursor.fetchone()

            data = {
                'success': 1,
                'user_id': result[0],
                'username': result[1],
            }
            session['user_id'] = data.get('user_id')
        else:
            data = {'success': 0}
        return jsonify(data)


@app.route('/checkemail', methods=['GET', 'POST'])
def checkEmail():
    if request.method == 'GET':
        return 'GET'
    else:
        email = request.form['email']

        sql = "select * from users where email=%s"
        res = cursor.execute(sql, (email,))
        if res:
            return jsonify({'has': 1})
        return jsonify({'has': 0})


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return 'GET'
    else:
        try:
            email = request.form['email']
            exam_id = request.form['exam_id']
            name = request.form['name']
            password = request.form['password']
            print(email, exam_id, name, password)
            sql = "insert into users (email, exam_id, realname, password, create_time, update_time) VALUES (%s,%s,%s,%s,now(),now())"

            cursor.execute(sql, (email, exam_id, name, password))
            db.commit()
            print('注册成功')
            form_data = {'success': 1}

        except Exception as e:
            print(e)
            db.rollback()
            form_data = {'success': 0}
        json_data = json.dumps(form_data)
        return json_data


@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': 1})


@app.route('/checkSession', methods=['POST'])
def checkSession():
    print('checkSession')
    session['user_id'] = '8'
    print(session.get('user_id'))
    user_id = session.get('user_id')
    if user_id:
        sql = 'select realname from users where id=%s'
        cursor.execute(sql, (user_id,))
        return jsonify({'success': 1, 'username': cursor.fetchone()[0]})
    return jsonify({'success': 0})


@app.route('/exam')
def exam():
    print(session.get('user_id'))
    session['user_id'] = '8'
    if session.get('user_id'):
        items = db.get_all_id(table_name='question')
        questions = []
        for i in items:
            items = db.get_data('question', i)
            questions.append(items.to_dict())

        return render_template('exam.html', question=questions)
    else:
        return render_template('temp.html')


@app.context_processor
def my_context():
    user_id = session.get('user_id')
    if user_id:
        sql = 'select realname from users where id = %s'
        cursor.execute(sql, (user_id,))
        name = cursor.fetchone()[0]
        return {'name': name, }
    else:
        return {}


@app.route('/admin')
def admin():
    if session.get('user_id') == 1:
        sql = 'select * from user_grade order by user_name,paper_id'
        cursor.execute(sql, )
        user_grade_data = cursor.fetchall()

        return render_template('admin.html', user_grade_data=user_grade_data)
    else:
        return render_template('temp.html')


@app.route('/analyze', methods=['get'])
def analyze_word():
    exam_item = ExamHelper()
    exam_item.initExam()
    res = exam_item.analyze()
    return jsonify(res)


@app.route('/submit_paper', methods=['post'])
def submit_paper():
    sum = 0
    data = request.form['answers']
    # for i in range(1,47):
    #     if (dict(data).get('{}'.format(i))):
    #         print(data[i])
    dict_data = dict(eval(data))
    for i in range(1, 46 * paper_id + 1):
        if dict_data.get('{}'.format(i)):
            sql = 'select id,answer,q_value from questions where id = %s and paper_id = %s'
            cursor.execute(sql, (i, paper_id))
            database = cursor.fetchone()
            trueAnswer = database.get('answer')
            yourAnser = dict_data.get('{}'.format(i))
            if trueAnswer == yourAnser:
                sum = sum + float(database.get('q_value'))
                # print('{}'.format(i),cursor.fetchone().get('answer'),dict_data.get('{}'.format(i)))

    sql = 'select * from docx where id = %s'
    cursor.execute(sql, (paper_id,))
    temp = cursor.fetchone()
    paper_name = temp.get('paper_name')

    sql = 'insert into user_grade (user_id, paper_id, exam_grade, create_time, paper_name,user_name) values (%s,%s,%s,now(), %s, %s)'
    cursor.execute(sql, (session.get('user_id'), paper_id, sum, paper_name, user_name))
    db.commit()
    return str(sum)


@app.route('/result')
def result():
    if session.get('user_id'):
        sql = 'select * from user_grade where user_id = %s'
        cursor.execute(sql, (session.get('user_id'),))
        user_grade = cursor.fetchall()

        return render_template('results.html', user_grade=user_grade)
    else:
        return render_template('temp.html')


# @app.route('/uploadfile/', methods=['post'])
# def uploadfile():
#     if session.get('user_id'):
#         papaername = request.form.get('papername')
#         if request.method == 'POST' and 'file' in request.files:
#             fileSet.save(request.files['file'], name=papaername + '.docx')
#             initDocx(papaername, papaername)
#             return redirect(url_for('admin'))
#         return '<script>alert("上传失败")</script>'
#     else:
#         return render_template('temp.html')


if __name__ == '__main__':
    app.run(debug=True, threaded=True, )
