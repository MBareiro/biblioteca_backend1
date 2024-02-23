from flask import jsonify, request
from app import app, db
from models.book_model import Book, BookSchema
from models.author_model import Author
from models.editorial_model import Editorial
from models.genre_model import Genre

book_schema = BookSchema()
books_schema = BookSchema(many=True)

@app.route('/books', methods=['GET'])
def get_books():
    try:
        all_books = Book.query.all()

        # Lista para almacenar resultados con nombres de autor, editorial y género
        books_with_names = []

        for book in all_books:
            # Consulta para obtener el nombre del autor
            author = Author.query.get(book.authors_id)
            author_name = author.name if author else "Author not found"

            # Consulta para obtener el nombre de la editorial
            editorial = Editorial.query.get(book.editorials_id)
            editorial_name = editorial.name if editorial else "Editorial not found"

            # Consulta para obtener el nombre del género
            genre = Genre.query.get(book.genres_id)
            genre_name = genre.name if genre else "Genre not found"

            # Convierte el objeto Book a un diccionario
            book_dict = book_schema.dump(book)

            # Agrega los nombres del autor, editorial y género al diccionario
            book_dict['authorName'] = author_name
            book_dict['editorialName'] = editorial_name
            book_dict['genreName'] = genre_name

            # Agrega el diccionario a la lista
            books_with_names.append(book_dict)

        return jsonify(books_with_names)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/books/<id>', methods=['GET'])
def get_book(id):
    book = Book.query.get(id)
    return book_schema.jsonify(book)

@app.route('/books/<id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if book:
        db.session.delete(book)
        db.session.commit()
        return book_schema.jsonify(book)
    else:
        return jsonify({'message': 'Book not found'}), 404

@app.route('/books', methods=['POST'])
def create_book():
    title = request.json['title']
    stock = request.json['stock']
    available = request.json['available']
    genre_id = request.json['genreId']
    author_id = request.json['authorId']
    editorial_id = request.json['editorialId']

    new_book = Book(
        title=title,
        stock=stock,
        available=available,
        genres_id=genre_id,
        authors_id=author_id,
        editorials_id=editorial_id
    )

    db.session.add(new_book)
    db.session.commit()

    return book_schema.jsonify(new_book)


@app.route('/books/<id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get(id)
    if book is None:
        return jsonify({'message': 'Book not found'}), 404

    book.title = request.json['title']
    book.stock = request.json['stock']
    book.available = request.json['available']
    book.genres_id = request.json['genre_id']
    book.authors_id = request.json['author_id']
    book.editorials_id = request.json['editorial_id']

    db.session.commit()
    return book_schema.jsonify(book)
