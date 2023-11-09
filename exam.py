#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project ：exam_system_python-flask
# @Time    : 2023/11/9 15:33
# @Author  : Hao
# @File    : exam.py
# @Description :
class ExamQuestion:

    def __init__(self, id, type, type_desc, question, options, solution, analysis, paper_name, paper_bonus, nth, issues_count, my_solution):
        self.id = id
        self.type = type
        self.type_desc = type_desc
        self.question = question
        self.options = options
        self.solution = solution
        self.analysis = analysis
        self.paper_name = paper_name
        self.paper_bonus = paper_bonus
        self.nth = nth
        self.issues_count = issues_count
        self.my_solution = my_solution

    # 设置id
    def set_id(self, id):
        self.id = id

    # 获取id
    def get_id(self):
        return self.id

    # 设置type
    def set_type(self, type):
        self.type = type

    # 获取type
    def get_type(self):
        return self.type

    # 设置type_desc
    def set_type_desc(self, type_desc):
        self.type_desc = type_desc

    # 获取type_desc
    def get_type_desc(self):
        return self.type_desc

    # 设置question
    def set_question(self, question):
        self.question = question

    # 获取question
    def get_question(self):
        return self.question

    # 设置options
    def set_options(self, options):
        self.options = options

    # 获取options
    def get_options(self):
        return self.options

    # 设置solution
    def set_solution(self, solution):
        self.solution = solution

    # 获取solution
    def get_solution(self):
        return self.solution

    # 设置analysis
    def set_analysis(self, analysis):
        self.analysis = analysis

    # 获取analysis
    def get_analysis(self):
        return self.analysis

    # 设置paper_name
    def set_paper_name(self, paper_name):
        self.paper_name = paper_name

    # 获取paper_name
    def get_paper_name(self):
        return self.paper_name

    # 设置paper_bonus
    def set_paper_bonus(self, paper_bonus):
        self.paper_bonus = paper_bonus

    # 获取paper_bonus
    def get_paper_bonus(self):
        return self.paper_bonus

    # 设置nth
    def set_nth(self, nth):
        self.nth = nth

    # 获取nth
    def get_nth(self):
        return self.nth

    # 设置issues_count
    def set_issues_count(self, issues_count):
        self.issues_count = issues_count

    # 获取issues_count
    def get_issues_count(self):
        return self.issues_count

    # 设置my_solution
    def set_my_solution(self, my_solution):
        self.my_solution = my_solution

    # 获取my_solution
    def get_my_solution(self):
        return self.my_solution
