from app import db

class Goods(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120), index = True, unique = True)
    count = db.Column(db.Integer, index = True)

    def __repr__(self):
        return '<Goods %r>' % (self.title)