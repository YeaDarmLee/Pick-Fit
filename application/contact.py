from flask import Flask, render_template, request
from flask import Blueprint
# import dbModule
from application import dbModule

contact = Blueprint("contact", __name__, url_prefix="/contact")

# contact
@contact.route("")
def index():
  return 'test'


@contact.route('/insert',methods=['POST'])
def insert_contact():
  
  try:
    name = request.form.get('name')
    message = request.form.get('message')

    if name == '' or message == '':
      return {
        'code':50000,
        'result': '모든 값을 입력해 주세요.'
      }
    
    db_class = dbModule.Database()
    search_user = "INSERT INTO contact_info(userNm,content) VALUES ('" + name + "','" + message + "');"

    db_class.execute(search_user)
    db_class.commit()

    return {
        'code':20000,
        'result': '등록이 완료되었습니다.'
      }
  except Exception as e:
    print(e)
    return {
        'code':50000,
        'result': e
      }