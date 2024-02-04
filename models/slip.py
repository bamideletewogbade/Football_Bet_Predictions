class Slip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    league = db.Column(db.String(100), nullable=False)
    teams = db.Column(db.String(100), nullable=False)
    tips = db.Column(db.String(100), nullable=False)
    posted_by = db.Column(db.String(100), nullable=False)
    bet_platform = db.Column(db.String(100), nullable=False)
    result = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(100), nullable=False)

   
