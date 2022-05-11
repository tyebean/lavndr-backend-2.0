
from api.models.db import db

class Conversation(db.Model):
  __tablename__ = 'conversations'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(500))
  image = db.Column(db.String())
  participants = db.Column(db.String())
  messages = db.Column(db.String(500))

  def __repr__(self):
    return f"Conversation('{self.id}', '{self.conversation}'"

  def serialize(self):
    conversation = {c.name: getattr(self, c.name) for c in self.__table__.columns}

    return conversation

