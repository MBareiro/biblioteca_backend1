from app import db, ma, app

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=True)
    stock = db.Column(db.Integer, nullable=True)
    available = db.Column(db.Integer, nullable=True)
    genres_id = db.Column(db.Integer, nullable=False)
    authors_id = db.Column(db.Integer, nullable=False)
    editorials_id = db.Column(db.Integer, nullable=False)

    def __init__(self, title, stock, available, genres_id, authors_id, editorials_id):
        self.title = title
        self.stock = stock
        self.available = available
        self.genres_id = genres_id
        self.authors_id = authors_id
        self.editorials_id = editorials_id

class BookSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'stock', 'available', 'genres_id', 'authors_id', 'editorials_id')

book_schema = BookSchema()
books_schema = BookSchema(many=True)

with app.app_context():
    db.create_all()
