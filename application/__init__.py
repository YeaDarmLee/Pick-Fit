from flask import Flask
from . import main
from . import join
from . import login
from . import crawler
from . import contact
from . import recommend

app = Flask(__name__)
app.secret_key="0d54679e-1522-11ec-82a8-0242ac130003"

app.register_blueprint(main.main)
app.register_blueprint(join.join)
app.register_blueprint(login.login)
app.register_blueprint(crawler.crawler)
app.register_blueprint(contact.contact)
app.register_blueprint(recommend.recommend)