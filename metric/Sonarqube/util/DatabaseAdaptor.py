# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 10:02:04 2019

@author: xv01171
"""

import mysql.connector
import json
from mysql.connector import errorcode

class DatabaseAdaptor:

    def readConfig(self, path):
        config = json.load(open(path))
        return config
    
    
    def getConnection(self, config):
        conn = None
        config['raise_on_warnings'] = True
        try:
            conn = mysql.connector.connect(**config)
        
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Cloud not connect to database - Access Denied")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

        return conn
    
    
    def executeQuery(self, connection, sql_query, parameter):
        cursor = connection.cursor()
        record = None
        try:
            cursor.execute(sql_query, parameter)
            record = cursor.fetchall()
            
        except mysql.connector.Error as err:
            print ("SQL-Error: ")
            print(err.msg)

        return record
    
    
    def insertIntoTable(self, connection, sql_query, parameter):
        cursor = connection.cursor()
        
        try:
            cursor.execute(sql_query, parameter)
            connection.commit()
        except mysql.connector.Error as err:
            print("SQL-Error: ")
            print(err.msg)

    
    def cleanUp(self, connection):
        connection.commit()
        connection.close()