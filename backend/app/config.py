import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_apscheduler import APScheduler
from models import db

load_dotenv(".env.local")

SUPABASE_URI = os.getenv("SUPABASE_URI")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

app = Flask(__name__)
CORS(app)

scheduler = APScheduler()

app.config["SQLALCHEMY_DATABASE_URI"] = f"{SUPABASE_URI}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SCHEDULER_API_ENABLED"] = True
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_pre_ping": True,
    "pool_recycle": 3600,
    "connect_args": {
        "keepalives": 1,
        "keepalives_idle": 30,
        "keepalives_interval": 10,
        "keepalives_count": 5,
    },
}


db.init_app(app)

scheduler.init_app(app)
