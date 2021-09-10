# 
# DB 접속시 아래 setting 맞춰주고 시작해야함
# host => slq 서버 주소
# user => slq 로그인 ID
# password => sql 로그인 PW
# db => 접속할 database 명
# 

import pymysql

class Database():
  def __init__(self):
    self.db = pymysql.connect(host='localhost',
                              user='root',
                              password='dldPekfa1!',
                              db='PICK_FIT',
                              charset='utf8')
    self.cursor = self.db.cursor(pymysql.cursors.DictCursor)

  def execute(self, query, args={}):
    self.cursor.execute(query, args)

  def executeOne(self, query, args={}):
    self.cursor.execute(query, args)
    row = self.cursor.fetchone()
    return row

  def executeAll(self, query, args={}):
    self.cursor.execute(query, args)
    row = self.cursor.fetchall()
    return row

  def commit(self):
    self.db.commit()

