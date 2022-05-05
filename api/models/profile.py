from datetime import datetime
from api.models.db import db

class Profile(db.Model):
    __tablename__ = 'profiles'
    # * Properties: 
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    name = db.Column(db.String(100), nullable=False)
    profile_picture = db.Column(db.String())
    dob = db.Column(db.Integer)
    gender_identity = db.Column(db.String())
    orientation = db.Column(db.String())
    location = db.Column(db.String)
    vibe_check = db.Column(db.String(200))
    bio = db.Column(db.String(500))
    sun_sign = db.Column('sun_sign', db.Enum('Ari', 'Tau', 'Gem', 'Can', 'Leo', 'Vir', 'Lib', 'Sco', 'Sag', 'Cap', 'Aqu', 'Pis', name='sun_type'))
    moon_sign = db.Column('moon_sign', db.Enum('Ari', 'Tau', 'Gem', 'Can', 'Leo', 'Vir', 'Lib', 'Sco', 'Sag', 'Cap', 'Aqu', 'Pis', name='moon_type'))
    rising_sign = db.Column('rising_sign', db.Enum('Ari', 'Tau', 'Gem', 'Can', 'Leo', 'Vir', 'Lib', 'Sco', 'Sag', 'Cap', 'Aqu', 'Pis', name='rising_type'))

    # * Relationships:
    messages = db.relationship("Message", secondary="messages", primaryjoin="Message.recipient_id==Profile.id", secondaryjoin="Message.sender_id==Profile.id")

    sent = db.relationship("Message", secondary="messages", primaryjoin="Message.sender_id==Profile.id", secondaryjoin="Message.recipient_id==Profile.id")

    def __repr__(self):
      return f"Profile('{self.id}', '{self.name}'"

    def serialize(self):
      profile = {c.name: getattr(self, c.name) for c in self.__table__.columns}

      messages = [message.serialize() for message in self.messages]
      sent = [message.serialize() for message in self.sent]

      profile['messages'] = messages 
      profile['sent'] = sent 

      return profile
