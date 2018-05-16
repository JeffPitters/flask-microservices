from app import db

class Staff(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120), index = True, unique = True)
    pswd = db.Column(db.String(60), index = True)
    rights = db.Column(db.SmallInteger)

    def __repr__(self):
        return '<Staff %r>' % (self.name)