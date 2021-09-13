from flask import Flask, render_template
from flask import Blueprint

join = Blueprint("join", __name__, url_prefix="/join")

# Join
@join.route("")
def index():
  return render_template('user/join.html')
