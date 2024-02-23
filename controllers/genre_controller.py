from flask import jsonify, request
from app import app, db
from models.genre_model import Genre, GenreSchema

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)

# Obtener todos los géneros
@app.route('/genres', methods=['GET'])
def get_genres():
    try:
        all_genres = Genre.query.all()
        result = genres_schema.dump(all_genres)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Obtener un género por su ID
@app.route('/genres/<id>', methods=['GET'])
def get_genre(id):
    genre = Genre.query.get(id)
    return genre_schema.jsonify(genre)

# Eliminar un género por su ID
@app.route('/genres/<id>', methods=['DELETE'])
def delete_genre(id):
    genre = Genre.query.get(id)
    if genre:
        db.session.delete(genre)
        db.session.commit()
        return genre_schema.jsonify(genre)
    else:
        return jsonify({'message': 'Genre not found'}), 404

# Crear un nuevo género
@app.route('/genres', methods=['POST'])
def create_genre():
    name = request.json['name']

    new_genre = Genre(
        name=name
    )

    db.session.add(new_genre)
    db.session.commit()

    return genre_schema.jsonify(new_genre)

# Actualizar un género por su ID
@app.route('/genres/<id>', methods=['PUT'])
def update_genre(id):
    genre = Genre.query.get(id)
    if genre is None:
        return jsonify({'message': 'Genre not found'}), 404

    genre.name = request.json['name']

    db.session.commit()
    return genre_schema.jsonify(genre)
