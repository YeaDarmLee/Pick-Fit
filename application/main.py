from flask import Flask, render_template, request, redirect, escape, session
from flask import Blueprint

# import dbModule
from application import dbModule

main = Blueprint("main", __name__, url_prefix="/")

@main.route("")
@main.route("/index")
def index():
  db_class = dbModule.Database()
  search_contact = "SELECT * FROM contact_info"
  data = db_class.executeAll(search_contact)

  # print(len(data))
  # for x in len(data):
  #   # detail_data = data[x]
  #   print(data[0])
  results = []
  for x in data:
    detail_data = []
    detail_data = dict(x)
    print(x)
    results.append({
      'idx':detail_data['idx'],
      'userNm':detail_data['userNm'],
      'content':detail_data['content'],
      'date':detail_data['c_date']
    })
  print(results)
  return render_template('index.html',contact_result=results)

@main.route("/myPage")
def myPage():
  userid = '%s' % escape(session['user_id'])

  db_class = dbModule.Database()
  search_user = "SELECT * FROM user_info where id = '" + userid + "';"
  data = dict(db_class.executeOne(search_user))

  return render_template('user/myPage.html', result=data)

@main.route("/urlReturnTest")
def urlReturnTest():
  # return redirect("http://192.168.100.195:9999/#portfolio")
  return redirect("/#portfolio")