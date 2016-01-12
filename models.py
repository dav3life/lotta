from __init__ import db


class Purchase(db.Model):
    __tablename__ = 'purchases'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    confirmed= db.Column(db.String)
    public_key = db.Column(db.String)
