from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import threading
import time
import requests

from config import Config
from routes import api_bp
from extensions import db  # Import db from extensions


load_dotenv()

app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins": "https://uttamm.web.app/"}, r"/api/*": {"methods": "POST"}})


app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

# Register the API blueprint
app.register_blueprint(api_bp, url_prefix='/api')

def ping_self():
    while True:
        try:
            with app.app_context():
              response = requests.get('https://contact-form-v2ph.onrender.com/api/test')
              print(f'Self-Ping Status: {response.status_code}')
        except requests.exceptions.RequestException as e:
            print(f'Self-Ping Error: {e}')
        time.sleep(1000)

ping_thread = None

@app.before_first_request
def before_first_request():
    global ping_thread
    if ping_thread is None:
        ping_thread = threading.Thread(target=ping_self, daemon=True)
        ping_thread.start()


@app.teardown_appcontext
def teardown_appcontext(exception=None):
    global ping_thread
    if ping_thread and ping_thread.is_alive():
        ping_thread.join(1)


if __name__ == '__main__':
    app.run(debug=True)