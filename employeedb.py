#!/usr/bin/env python3
# coding: utf-8

# Copyright (c) Latona. All rights reserved.

import json
import os
import sys
import MySQLdb

# AION共通モジュール
#import aion.mysql as mysql
from StatusJsonPythonModule import StatusJsonRest

BASE_PATH = os.path.join(os.path.dirname(__file__), )

class EmployeeDB():
    def __init__(self):
        settings = json.load(
            open(os.path.join(os.path.dirname(__file__), 'mysql-config.json'), 'r')
        )
        self.connection = MySQLdb.connect(
            host=settings.get('host'),
            user=settings.get('user'),
            passwd=settings.get('password'),
            db='FaceRecognition',
            charset='utf8')
        self.cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)

    def getEmployeeFromID(self, employee_id):
        sql = """
            select 
                employee_id,
                name,
                department,
                position
            from FaceRecognition.employee
            where employee_id=%d;
        """ % (employee_id, )
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def insertEmployee(self, employee_id, name, department, position):
        sql = """ 
            insert into FaceRecognition.employee 
            (employee_id, name, department, position) 
            values 
            (%d, '%s', '%s', '%s'); 
            """ % (employee_id, name, department, position)
        self.cursor.execute(sql)
        self.connection.commit()

    def insertPersonID(self, employee_id, person_id):
        sql = """ 
            insert into FaceRecognition.person_id 
            (employee_id, person_id) 
            values 
            (%d, '%s'); 
            """ % (employee_id, person_id)
        self.cursor.execute(sql)
        self.connection.commit()

    def insertImages(self, employee_id, image_number, image_path):
        sql = """ 
            insert into FaceRecognition.images 
            (employee_id, image_number, image_path) 
            values 
            (%d, %d, '%s'); 
            """ % (employee_id, image_number, image_path)
        self.cursor.execute(sql)
        self.connection.commit()

    def deleteAll(self):
        sql1 = "truncate FaceRecognition.images;"
        sql2 = "truncate FaceRecognition.person_id;"
        sql3 = "truncate FaceRecognition.employee;"
        print("delete database images")
        self.cursor.execute(sql1)
        self.connection.commit()
        print("delete database person_id")
        self.cursor.execute(sql2)
        self.connection.commit()
        print("delete database employee")
        self.cursor.execute(sql3)
        self.connection.commit()
        

