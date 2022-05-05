from flask import Blueprint, jsonify, request
from api.middleware import login_required, read_token

from api.models.db import db
from api.models.message import Message

messages = Blueprint('messages', 'message')

# * create a msg
@messages.route('/<recipient_id>', methods=["POST"])
@login_required
def create(recipient_id):
  data = request.get_json()
  profile = read_token(request)
  data["sender_id"] = profile["id"]
  data["recipient_id"] = recipient_id

  message = Message(**data)
  db.session.add(message)
  db.session.commit()
  return jsonify(message.serialize()), 201

# * index all msgs
@messages.route('/', methods=["GET"])
@login_required
def index():
  messages = Message.query.all()
  return jsonify([message.serialize() for message in messages]), 200 

# show a msg - @login_required
@messages.route('/<id>', methods=["GET"])
@login_required
def show(id):
  message = Message.query.filter_by(id=id).first()
  message_data = message.serialize()
  return jsonify(message=message_data), 200

# update msg
@messages.route('/<id>', methods=["PUT"]) 
@login_required
def update(id):
  data = request.get_json()
  profile = read_token(request)
  message = Message.query.filter_by(id=id).first()

  if message.sender_id != profile["id"]:
    return 'Forbidden', 403

  for key in data:
    setattr(message, key, data[key])

  db.session.commit()
  return jsonify(message.serialize()), 200

# delete msg
@messages.route('/<id>', methods=["DELETE"]) 
@login_required
def delete(id):
  profile = read_token(request)
  message = Message.query.filter_by(id=id).first()

  if message.sender_id != profile["id"]:
    return 'Forbidden', 403

  db.session.delete(message)
  db.session.commit()
  return jsonify(message="Success"), 200