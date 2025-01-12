from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from config import Config
from routes import api_bp
from extensions import db
from flask_apscheduler import APScheduler
import requests
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = Flask(__name__)
scheduler = APScheduler()

# CORS configuration
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://uttamm.web.app/", "https://contact-form-v2ph.onrender.com/"],
        "methods": ["POST", "GET"]
    }
})

app.config.from_object(Config)

# Add APScheduler configurations
app.config.update(
    SCHEDULER_API_ENABLED=True,
    SCHEDULER_TIMEZONE="UTC"
)

db.init_app(app)

# Initialize scheduler with Flask app
scheduler.init_app(app)

def keep_alive():
    """
    Function to make a request to the application to keep it alive
    """
    try:
        # Replace with your actual application URL on Render
        response = requests.get('https://contact-form-v2ph.onrender.com/api/health')
        logger.info(f"Keep-alive ping sent. Status: {response.status_code}")
    except Exception as e:
        logger.error(f"Keep-alive request failed: {str(e)}")

# Add scheduled job
@scheduler.task('interval', id='keep_alive_job', minutes=14, misfire_grace_time=None)
def schedule_keep_alive():
    with app.app_context():
        keep_alive()

# Start the scheduler
scheduler.start()

with app.app_context():
    db.create_all()

# Register the API blueprint
app.register_blueprint(api_bp, url_prefix='/api')

# Add a health check endpoint
@app.route('/api/health')
def health_check():
    return {'status': 'healthy'}, 200

if __name__ == '__main__':
    app.run(debug=True)