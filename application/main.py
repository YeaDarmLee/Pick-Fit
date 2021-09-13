from flask import Flask, render_template, request, redirect
from flask import Blueprint

# import dbModule
from application import dbModule

main = Blueprint("main", __name__, url_prefix="/")

@main.route("")
def index():
  return render_template('index.html')

@main.route("/test")
def test():
  db_class = dbModule.Database()
  search_url_info = "SELECT * FROM url_info;"
  url_info_result = db_class.executeAll(search_url_info)

  result = []
  for i in url_info_result:
    result.append(i)

  return {'result': result}

@main.route("/urlReturnTest")
def urlReturnTest():
  # return redirect("http://192.168.100.195:9999/#portfolio")
  return redirect("/#portfolio")