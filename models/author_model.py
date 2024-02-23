from app import db, ma, app

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=True)
    last_name = db.Column(db.String(45), nullable=True)

    def __init__(self, name, last_name):
        self.name = name
        self.last_name = last_name

class AuthorSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'last_name')

author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True)

with app.app_context():
    db.create_all()
