from flask import Blueprint, jsonify, request
from api.middleware import login_required, read_token

from api.models.db import db
from api.models.profile import Profile
from api.models.message import Message

import os 

profiles = Blueprint('profiles', 'profile')

# * index all profs
@profiles.route('/', methods=["GET"])
def index():
  profiles = Profile.query.all()
  return jsonify([profile.serialize() for profile in profiles]), 200

# * show one prof
@profiles.route('/<id>', methods=["GET"])
def show(id):
  profile = Profile.query.filter_by(id=id).first()
  profile_data = profile.serialize()
  return jsonify(profile=profile_data), 200

# * update the prof
@profiles.route('/<id>', methods=["PUT"]) 
@login_required
def update(id):
  data = request.get_json()
  user = read_token(request)
  profile = Profile.query.filter_by(id=id).first()

  if profile.user_id != user["id"]:
    return 'Forbidden', 403

  for key in data:
    setattr(profile, key, data[key])
  db.session.commit()
  return jsonify(profile.serialize()), 200

# * delete the prof
@profiles.route('/<id>', methods=["DELETE"])
@login_required
def delete(id):
  user = read_token(request)
  profile = Profile.query.filter_by(id=id).first()

  if profile.user_id != user["id"]:
    return 'Forbidden', 403
  
  db.session.delete(profile)
  db.session.commit()
  return jsonify(message="Success"), 200


# @profiles.route("/<id>", methods=['POST'])
# def upload_file():
#   profiles.logger.info('in upload route')

#   cloudinary.config(cloud_name = os.getenv('CLOUD_NAME'), api_key=os.getenv('API_KEY'), 
#     api_secret=os.getenv('API_SECRET'))
#   upload_result = None
#   if request.method == 'POST':
#     file_to_upload = request.files['file']
#     profiles.logger.info('%s file_to_upload', file_to_upload)
#     if file_to_upload:
#       upload_result = cloudinary.uploader.upload(file_to_upload)
#       profiles.logger.info(upload_result)
#       return jsonify(upload_result)