from flask import jsonify, request
from app import app, db
from models.beneficiary_model import Beneficiary, BeneficiarySchema
from models.suscription_model import Subscription

beneficiary_schema = BeneficiarySchema()
beneficiaries_schema = BeneficiarySchema(many=True)

@app.route('/beneficiaries', methods=['GET'])
def get_beneficiaries():
    try:
        all_beneficiaries = Beneficiary.query.all()
        result = beneficiaries_schema.dump(all_beneficiaries)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/beneficiaries/<id>', methods=['GET'])
def get_beneficiary(id):
    beneficiary = Beneficiary.query.get(id)
    return beneficiary_schema.jsonify(beneficiary)

@app.route('/beneficiaries/<id>', methods=['DELETE'])
def delete_beneficiary(id):
    beneficiary = Beneficiary.query.get(id)
    if beneficiary:
        # Obtener la suscripción del beneficiario
        subscription = Subscription.query.filter_by(id_user=id).first()

        # Eliminar la suscripción si existe
        if subscription:
            db.session.delete(subscription)
            db.session.commit()  # Confirmar la eliminación de la suscripción

        # Eliminar el beneficiario
        db.session.delete(beneficiary)
        db.session.commit()  # Confirmar la eliminación del beneficiario

        return beneficiary_schema.jsonify(beneficiary)
    else:
        return jsonify({'message': 'Beneficiary not found'}), 404



@app.route('/beneficiaries', methods=['POST'])
def create_beneficiary():
    name = request.json['name']
    last_name = request.json['last_name']
    phone = request.json['phone']

    new_beneficiary = Beneficiary(
        name=name,
        last_name=last_name,
        phone=phone,
    )

    db.session.add(new_beneficiary)
    db.session.commit()

    return beneficiary_schema.jsonify(new_beneficiary)

@app.route('/beneficiaries/<id>', methods=['PUT'])
def update_beneficiary(id):
    beneficiary = Beneficiary.query.get(id)
    if beneficiary is None:
        return jsonify({'message': 'Beneficiary not found'}), 404

    beneficiary.name = request.json['name']
    beneficiary.last_name = request.json['last_name']
    beneficiary.phone = request.json['phone']

    db.session.commit()
    return beneficiary_schema.jsonify(beneficiary)
