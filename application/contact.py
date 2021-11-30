from flask import Flask, render_template, request
from flask import Blueprint
# import dbModule
from application import dbModule

contact = Blueprint("contact", __name__, url_prefix="/contact")

# contact
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
    
    checkNm = name.replace(" ","")
    checkMg = message.replace(" ","")
    if checkNm == '' or checkMg == '':
      return {
        'code':50000,
        'result': '공백은 입력할 수 없습니다.'
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

@contact.route("/getContactList",methods=['POST'])
def getContactList():
  try:
    db_class = dbModule.Database()
    search_contact = "SELECT * FROM contact_info ORDER BY idx DESC limit 100;"
    data = db_class.executeAll(search_contact)

    results = []
    for x in data:
      detail_data = []
      detail_data = dict(x)
      results.append({
        'idx':detail_data['idx'],
        'userNm':detail_data['userNm'],
        'content':detail_data['content'],
        'date1': detail_data['c_date'].strftime('%Y-%m-%d'),
        'date2': detail_data['c_date'].strftime('%H:%M:%S')
      })
    print(results)

    return {
      'code':20000,
      'results':results
    }
  except Exception as e:
    print(e)
    return {
        'code':50000,
        'result': e
      }