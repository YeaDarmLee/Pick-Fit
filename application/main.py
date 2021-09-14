from flask import Flask, render_template, request, redirect
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

  return render_template('user/myPage.html')

@main.route("/urlReturnTest")
def urlReturnTest():
  # return redirect("http://192.168.100.195:9999/#portfolio")
  return redirect("/#portfolio")