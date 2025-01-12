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

# Define a list of allowed origins for CORS
allowed_origins = ["https://uttamm.web.app", "https://contact-form-v2ph.onrender.com"]  # Add more as needed

# Configure CORS with multiple origins
CORS(app, resources={r"/api/*": {"origins": allowed_origins}},  methods=["POST"])

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
ping_thread_started = False  # Track if ping thread is already running


@app.before_first_request
def before_first_request():
    global ping_thread, ping_thread_started
    if not ping_thread_started:
        ping_thread = threading.Thread(target=ping_self, daemon=True)
        ping_thread.start()
        ping_thread_started = True  # Set flag to true once started



@app.teardown_appcontext
def teardown_appcontext(exception=None):
    global ping_thread
    if ping_thread and ping_thread.is_alive():
        ping_thread.join(1)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)  # Allow external access with host and port, use 0.0.0.0 for external traffic