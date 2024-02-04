from app import db

class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    league = db.Column(db.String(50), nullable=False)
    teams = db.Column(db.String(50), nullable=False)
    tips = db.Column(db.Text, nullable=False)
    result = db.Column(db.boolean, nullable=False)
    posted_by = db.Column(db.String(20), nullable=True)

    def __repr__(self):
        return f'<Prediction {self.id}>'
