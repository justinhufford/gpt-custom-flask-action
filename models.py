from app import db

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    strength = db.Column(db.Float, default=0.8)
    accuracy = db.Column(db.Float, default=0.8)
    swing_power = db.Column(db.Float, default=1.0)
    inventory = db.relationship('Item', backref='player', lazy=True)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    bio = db.Column(db.String(255), nullable=True)
    potential = db.Column(db.Float, nullable=False)
    mass = db.Column(db.Float, nullable=False)
    condition = db.Column(db.Float, nullable=False)
    decay = db.Column(db.Float, nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
