



from flask import Flask
from app.routes.health import health_bp
from app.routes.address import address_bp
from app.routes.btc import btc_bp
from app.models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cointracker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
app.register_blueprint(health_bp)
app.register_blueprint(address_bp)
app.register_blueprint(btc_bp)

@app.route('/')
def home():
    return 'Hello, Flask!'
