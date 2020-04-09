# -*- coding: utf-8 -*-
"""
@author: Recep Balbay
"""


from datetime import datetime
from time import sleep
import mysql.connector as mariadb

__author__ = 'Recep BALBAY'
__copyright__ = 'Copyright 2019, DAG-MAM Project'
__license__ = 'GPL'
__version__ = '1.1.1'
__maintainer__  = 'Recep BALBAY'
__email__ = 'rbalbay@gmail.com'
__status__ = 'In Development'
starting_value = True


class SeeingMonitor:
    def __init__(self):
        self.sql_query = "INSERT INTO `2020` (`date`, `seeing`) VALUES (%s, %s)"
        self.last_seeing_data_txt = "C:\\Users\\SM\\Documents\\MiniCyclop\\Data\\Last_Seeing_Data.txt"
        self.seeing_sql_date = ''
        self.last_seeing_value = ''

    @staticmethod
    def get_time():
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def read_last_seeing_data(self):
        seeing_date = []
        seeing_time = []
        last_seeing_value = []

        with open(self.last_seeing_data_txt, 'r') as data:
            line = data.readlines()
            seeing_date.append(line[0].split('|')[0].split()[0].strip())
            seeing_time.append(line[0].split('|')[0].split()[1].strip())
            last_seeing_value.append(line[0].split('|')[4].strip())

        seeing_day = seeing_date[0].split('.')[0]
        if len(seeing_day) < 2:
            seeing_day = '0' + seeing_day

        seeing_month = seeing_date[0].split('.')[1]
        if len(seeing_month) < 2:
            seeing_month = '0' + seeing_month

        seeing_year = seeing_date[0].split('.')[2]
        seeing_sql_date = seeing_year + '-' + seeing_month + '-' + seeing_day + ' ' + str(seeing_time[0])

        self.seeing_sql_date = seeing_sql_date
        self.last_seeing_value = last_seeing_value[0]

    def sql_upload(self):
        sql_seeing = (self.seeing_sql_date, self.last_seeing_value)

        try:
            db_MAM = mariadb.connect(
                host="",                    # Server IP adres
                user="",                    # Username
                passwd="",                  # Password
                database="seeing")

            db_MAM_cursor = db_MAM.cursor()
            db_MAM_cursor.execute(self.sql_query, sql_seeing)
            db_MAM.commit()

            print(self.get_time() + ' | Seeing data uploaded.')

        except Exception as sqlError:
            print(getattr(sqlError, 'message', repr(sqlError)))


if __name__ == '__main__':
    sm = SeeingMonitor()
    while True:
        if starting_value:
            print(sm.get_time() + ' | ATASAM Cyclope Seeing Monitor Control Software %s' % __version__)
            print(sm.get_time() + ' | ----------------------------------------------------')
            starting_value = False
            sleep(1)
        else:
            try:
                sm.read_last_seeing_data()
                sleep(1)
            except Exception as e:
                print(getattr(e, 'message', repr(e)))

            sleep(1)

            try:
                sm.sql_upload()
                sleep(1)
            except Exception as e:
                print(getattr(e, 'message', repr(e)))

            sleep(10)
