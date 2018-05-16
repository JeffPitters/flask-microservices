from app import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120), index = True, unique = True)
    mail = db.Column(db.String(120), index = True, unique = True)
    pswd = db.Column(db.String(60), index = True)

    def __repr__(self):
        return '<Customer %r>' % (self.name)