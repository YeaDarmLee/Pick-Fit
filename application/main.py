from flask import Flask, render_template, request, redirect, escape, session
from flask import Blueprint

# import dbModule
from application import dbModule

main = Blueprint("main", __name__, url_prefix="/")

@main.route("")
def index():
  return render_template('index.html')

@main.route("/index")
def index2():
  return render_template('index.html')

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