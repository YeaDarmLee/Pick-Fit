from flask import Flask, render_template, request, redirect, escape, session
from flask import Blueprint

# import dbModule
from application import dbModule

main = Blueprint("main", __name__, url_prefix="/")

@main.route("")
@main.route("/index")
def index():
  return render_template('index.html')

@main.route("/myPage")
def myPage():
  try:
    userid = '%s' % escape(session['user_id'])

    db_class = dbModule.Database()
    search_user = "SELECT * FROM user_info where id = '" + userid + "';"
    data = dict(db_class.executeOne(search_user))

    return render_template('user/myPage.html', result=data)
  except Exception as e:
    print(e)
    return render_template('layout/error.html')

@main.route("/getContactList",methods=['POST'])
def getContactList():
  try:
    db_class = dbModule.Database()
    search_contact = "SELECT * FROM contact_info"
    data = db_class.executeAll(search_contact)

    results = []
    for x in data:
      detail_data = []
      detail_data = dict(x)
      results.append({
        'idx':detail_data['idx'],
        'userNm':detail_data['userNm'],
        'content':detail_data['content'],
        'date':detail_data['c_date']
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

@main.route("/urlReturnTest")
def urlReturnTest():
  import os
  import sys
  import urllib.request
  client_id = "rtBTN3ODWGI6wia_xLWo"
  client_secret = "6K3Kkygf5m"
  url = "https://openapi.naver.com/v1/datalab/search"
  body = '{"startDate":"2017-01-01","endDate":"2017-04-30","timeUnit":"month","keywordGroups":[{"groupName":"닌텐도","keywords":["스위치","korean"]}],"device":"pc","ages":["1"],"gender":"m"}'

  request = urllib.request.Request(url)
  request.add_header("X-Naver-Client-Id",client_id)
  request.add_header("X-Naver-Client-Secret",client_secret)
  request.add_header("Content-Type","application/json")
  response = urllib.request.urlopen(request, data=body.encode("utf-8"))
  rescode = response.getcode()
  if(rescode==200):
      response_body = response.read()
      print(response_body.decode('utf-8'))
  else:
      print("Error Code:" + rescode)

  return(response_body.decode('utf-8'))
  