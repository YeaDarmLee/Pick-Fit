from flask import Flask
from . import main
from . import join
from . import login
from . import crawler

app = Flask(__name__)

app.register_blueprint(main.main)
app.register_blueprint(join.join)
app.register_blueprint(login.login)
app.register_blueprint(crawler.crawler)