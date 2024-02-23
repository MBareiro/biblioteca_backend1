from flask import jsonify, request
from app import app, db
from models.author_model import Author, AuthorSchema

author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True)

@app.route('/authors', methods=['GET'])
def get_authors():
    try:
        all_authors = Author.query.all()
        result = authors_schema.dump(all_authors)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/authors/<id>', methods=['GET'])
def get_author(id):
    author = Author.query.get(id)
    return author_schema.jsonify(author)

@app.route('/authors/<id>', methods=['DELETE'])
def delete_author(id):
    author = Author.query.get(id)
    if author:
        db.session.delete(author)
        db.session.commit()
        return author_schema.jsonify(author)
    else:
        return jsonify({'message': 'Author not found'}), 404

@app.route('/authors', methods=['POST'])
def create_author():
    name = request.json['name']
    last_name = request.json['last_name']

    new_author = Author(
        name=name,
        last_name=last_name
    )

    db.session.add(new_author)
    db.session.commit()

    return author_schema.jsonify(new_author)

@app.route('/authors/<id>', methods=['PUT'])
def update_author(id):
    author = Author.query.get(id)
    if author is None:
        return jsonify({'message': 'Author not found'}), 404

    author.name = request.json['name']
    author.last_name = request.json['last_name']

    db.session.commit()
    return author_schema.jsonify(author)
