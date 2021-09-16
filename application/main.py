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
    user_data = dict(db_class.executeOne(search_user))
    
    search_log = "SELECT * FROM search_log where user_id = '" + userid + "';"
    log_data = db_class.executeAll(search_log)

    results = []
    for x in log_data:
      s_type = ''
      detail_data = []
      detail_data = dict(x)
      if detail_data['s_type'] == 'tn':
        s_type = '트렌드 조회'
      elif detail_data['s_type'] == 'co':
        s_type = '의류 추천'
      elif detail_data['s_type'] == 'cl':
        s_type = '크롤링'
      elif detail_data['s_type'] == 'st':
        s_type = '통계 조회'
      
      results.append({
        'idx':detail_data['idx'],
        's_type':s_type,
        'user_id':detail_data['user_id'],
        'date':detail_data['c_date']
      })

    return render_template('user/myPage.html', user=user_data, log=results)

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
  