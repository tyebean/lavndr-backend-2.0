from datetime import datetime
from api.models.db import db

class Message(db.Model):
  __tablename__ = 'messages'
  id = db.Column(db.Integer, primary_key=True)
  content = db.Column(db.String(500))
  sent_at = db.Column(db.DateTime, default=datetime.utcnow)

  recipient_id = db.Column(db.Integer, db.ForeignKey('profiles.id'))
  sender_id = db.Column(db.Integer, db.ForeignKey('profiles.id'))

  def __repr__(self):
    return f"Message('{self.id}', '{self.message}'"

  def serialize(self):
    message = {c.name: getattr(self, c.name) for c in self.__table__.columns}

    return message