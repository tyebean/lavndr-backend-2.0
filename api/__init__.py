from distutils.command.upload import upload
from flask import Flask 
from flask_cors import CORS, cross_origin
from flask_migrate import Migrate
from api.models.db import db
from config import Config


# ============ Import Models ============
from api.models.user import User
from api.models.profile import Profile
from api.models.message import Message

# ============ Import Views ============
from api.views.auth import auth
from api.views.profiles import profiles
from api.views.message import messages


cors = CORS()
migrate = Migrate() 
list = ['GET', 'HEAD', 'POST', 'OPTIONS', 'PUT', 'PATCH', 'DELETE', 'LINK']

def create_app(config):
  app = Flask(__name__)
  app.config.from_object(config)


  db.init_app(app)
  migrate.init_app(app, db)
  cors.init_app(app, supports_credentials=True, methods=list)

  # ============ Register Blueprints ============
  app.register_blueprint(auth, url_prefix='/api/auth') 
  app.register_blueprint(profiles, url_prefix='/api/profiles')
  app.register_blueprint(messages, url_prefix='/api/messages')

  return app

app = create_app(Config)