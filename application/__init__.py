from flask import Flask
from . import main
from . import user
from . import contact
from . import recommend

app = Flask(__name__)

# 세션 secret_key
app.secret_key="0d54679e-1522-11ec-82a8-0242ac130003"

app.register_blueprint(main.main)
app.register_blueprint(user.user)
app.register_blueprint(contact.contact)
app.register_blueprint(recommend.recommend)