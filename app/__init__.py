from flask import Flask
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import views




@app.cli.command("seed-db")
def seed_db_command():
    """Seed the database with test data."""
    from app.seed_data import seed_database
    seed_database()