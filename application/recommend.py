from flask import Flask, render_template, request
from flask import Blueprint

recommend = Blueprint("recommend", __name__, url_prefix="/recommend")

# recommend
@recommend.route("")
def index():
  return render_template('recommend/recommend.html')

@recommend.route("/trend")
def trend():
  return render_template('recommend/trend.html')

