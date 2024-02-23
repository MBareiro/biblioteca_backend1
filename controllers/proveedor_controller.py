from flask import jsonify, request
from app import db, app
from models.proveedor_model import Proveedor, ProveedorSchema

proveedor_schema = ProveedorSchema()
proveedores_schema = ProveedorSchema(many=True)

@app.route('/proveedores', methods=['GET'])
def get_proveedores():
    try:
        all_proveedores = Proveedor.query.all()

        # Convierte los nombres a primera letra en mayúscula
        for proveedor in all_proveedores:
            proveedor.nombre = proveedor.nombre.capitalize()
            proveedor.direccion = proveedor.direccion.capitalize()

        result = proveedores_schema.dump(all_proveedores)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/proveedores/<id>', methods=['GET'])
def get_proveedor(id):
    print("esta es")
    proveedor = Proveedor.query.get(id)
    proveedor.nombre = proveedor.nombre.capitalize()
    proveedor.direccion = proveedor.direccion.capitalize()
    return proveedor_schema.jsonify(proveedor)

@app.route('/proveedores/<id>', methods=['DELETE'])
def delete_proveedor(id):
    proveedor = Proveedor.query.get(id)
    if proveedor:
        db.session.delete(proveedor)
        db.session.commit()
        return proveedor_schema.jsonify(proveedor)
    else:
        return jsonify({'message': 'Proveedor no encontrado'}), 404

@app.route('/proveedores', methods=['POST'])
def create_proveedor():
    nombre = request.json['nombre']
    telefono = request.json['telefono']
    direccion = request.json['direccion']

    nombre = nombre.lower()

    new_proveedor = Proveedor(
        nombre=nombre,
        telefono=telefono,
        direccion=direccion
    )

    db.session.add(new_proveedor)
    db.session.commit()

    return proveedor_schema.jsonify(new_proveedor)

@app.route('/proveedores/<id>', methods=['PUT'])
def update_proveedor(id):
    print("aca entro")
    proveedor = Proveedor.query.get(id)
    if proveedor is None:
        return jsonify({'message': 'Proveedor no encontrado'}), 404

    proveedor.nombre = request.json['nombre']
    proveedor.telefono = request.json['telefono']
    proveedor.direccion = request.json['direccion']

    db.session.commit()
    return proveedor_schema.jsonify(proveedor)
