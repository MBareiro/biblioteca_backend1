from app import db, ma, app

class Editorial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=True)

    def __init__(self, name):
        self.name = name

class EditorialSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')

editorial_schema = EditorialSchema()
editorials_schema = EditorialSchema(many=True)

with app.app_context():
    db.create_all()
