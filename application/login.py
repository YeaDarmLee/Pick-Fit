from flask import Flask, render_template
from flask import Blueprint

login = Blueprint("login", __name__, url_prefix="/login")

# Login
@login.route("")
def index():
  return render_template('user/login.html')
