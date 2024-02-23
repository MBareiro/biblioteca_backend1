from app import db, ma, app

class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=True)

    def __init__(self, name):
        self.name = name

class GenreSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)

with app.app_context():
    db.create_all()
