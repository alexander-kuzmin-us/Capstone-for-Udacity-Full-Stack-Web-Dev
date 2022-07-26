from app import db


class Charter(db.Model):
    __tablename__ = 'charters'
    id = db.Column(db.Integer, primary_key=True)
    charters_name = db.Column(db.String)
    departure_date = db.Column(db.Date)
    skippers = db.relationship('Skipper', backref='charters')

    def format(self):
        return {
            'id': self.id,
            'charters_name': self.charters_name,
            'departure_date': self.departure_date,
            'skippers': self.skippers
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Skipper(db.Model):
    __tablename__ = 'skippers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    gender = db.Column(db.String)
    charter_id = db.Column(db.Integer, db.ForeignKey('charters.id'), nullable=False)

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'charter_id': self.charter_id
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


# db.create_all()