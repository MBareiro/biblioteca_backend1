from flask import jsonify, request
from app import app, db
from models.editorial_model import Editorial, EditorialSchema

editorial_schema = EditorialSchema()
editorials_schema = EditorialSchema(many=True)

# Obtener todas las editoriales
@app.route('/editorials', methods=['GET'])
def get_editorials():
    try:
        all_editorials = Editorial.query.all()
        result = editorials_schema.dump(all_editorials)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Obtener una editorial por su ID
@app.route('/editorials/<id>', methods=['GET'])
def get_editorial(id):
    editorial = Editorial.query.get(id)
    return editorial_schema.jsonify(editorial)

# Eliminar una editorial por su ID
@app.route('/editorials/<id>', methods=['DELETE'])
def delete_editorial(id):
    editorial = Editorial.query.get(id)
    if editorial:
        db.session.delete(editorial)
        db.session.commit()
        return editorial_schema.jsonify(editorial)
    else:
        return jsonify({'message': 'Editorial not found'}), 404

# Crear una nueva editorial
@app.route('/editorials', methods=['POST'])
def create_editorial():
    name = request.json['name']

    new_editorial = Editorial(
        name=name
    )

    db.session.add(new_editorial)
    db.session.commit()

    return editorial_schema.jsonify(new_editorial)

# Actualizar una editorial por su ID
@app.route('/editorials/<id>', methods=['PUT'])
def update_editorial(id):
    editorial = Editorial.query.get(id)
    if editorial is None:
        return jsonify({'message': 'Editorial not found'}), 404

    editorial.name = request.json['name']

    db.session.commit()
    return editorial_schema.jsonify(editorial)
