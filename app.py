# app.py
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

from config import Config
from routes import api_bp
from extensions import db  # Import db from extensions


load_dotenv()

app = Flask(__name__)
#CORS(app)
# Implement cors for specific origin and methods
CORS(app, resources={r"/api/*": {"origins": "https://uttamm.web.app/"}, r"/api/*": {"methods": "POST"}})


app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

# Register the API blueprint
app.register_blueprint(api_bp, url_prefix='/api')


if __name__ == '__main__':
    app.run(debug=True)