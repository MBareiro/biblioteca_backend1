import datetime
from flask import request, jsonify
from app import app, db
from models.beneficiary_model import Beneficiary
from models.suscription_model import Subscription, SubscriptionSchema

subscription_schema = SubscriptionSchema()
subscriptions_schema = SubscriptionSchema(many=True)

# Endpoint para crear una nueva suscripción
@app.route('/subscription', methods=['POST'])
def add_subscription():
    # Obtener los datos de la solicitud JSON
    start_date_str = request.json['start_date']
    end_date_str = request.json['end_date']
    id_user = request.json['id_user']

    # Convertir las cadenas de fecha y hora al formato adecuado
    start_date = datetime.fromisoformat(start_date_str.replace('Z', '+00:00'))
    end_date = datetime.fromisoformat(end_date_str.replace('Z', '+00:00'))

    # Crear una nueva instancia de Subscription con los datos proporcionados
    new_subscription = Subscription(start_date=start_date, end_date=end_date, id_user=id_user)

    # Agregar la nueva suscripción a la sesión de la base de datos y confirmar los cambios
    db.session.add(new_subscription)
    db.session.commit()

    # Devolver los datos de la nueva suscripción en formato JSON
    return subscription_schema.jsonify(new_subscription)

# Endpoint para obtener todas las suscripciones con el nombre y apellido del beneficiario
@app.route('/subscriptions', methods=['GET'])
def get_subscriptions():
    # Realizar una operación de unión entre las tablas Subscription y Beneficiary
    subscriptions_with_names = db.session.query(Subscription.id, Subscription.start_date, Subscription.end_date, Subscription.id_user, Beneficiary.name, Beneficiary.last_name) \
        .join(Beneficiary, Subscription.id_user == Beneficiary.id) \
        .all()

    # Convertir el resultado en un formato JSON
    result = []
    for subscription in subscriptions_with_names:
        subscription_dict = {
            "id": subscription.id,
            "start_date": subscription.start_date.strftime("%Y-%m-%dT%H:%M:%S"),
            "end_date": subscription.end_date.strftime("%Y-%m-%dT%H:%M:%S"),
            "name": subscription.name,
            "last_name": subscription.last_name
        }
        result.append(subscription_dict)

    return jsonify(result)

# Endpoint para obtener una suscripción por ID de usuario (id_user)
@app.route('/subscription/<id_user>', methods=['GET'])
def get_subscription(id_user):
    subscription = Subscription.query.filter_by(id_user=id_user).first()
    if subscription:
        return subscription_schema.jsonify(subscription)
    else:
        return jsonify({'message': 'Subscription not found'}), 404


# Endpoint para actualizar una suscripción por ID
@app.route('/subscription/<id>', methods=['PUT'])
def update_subscription(id):
    subscription = Subscription.query.get(id)

    start_date = request.json['start_date']
    end_date = request.json['end_date']

    subscription.start_date = start_date
    subscription.end_date = end_date

    db.session.commit()
    return subscription_schema.jsonify(subscription)

# Endpoint para eliminar una suscripción por ID
@app.route('/subscription/<id>', methods=['DELETE'])
def delete_subscription(id):
    subscription = Subscription.query.get(id)
    db.session.delete(subscription)
    db.session.commit()

    return subscription_schema.jsonify(subscription)

# Endpoint para verificar la existencia de una suscripción por ID de usuario
@app.route('/subscription/check/<id_user>', methods=['GET'])
def check_existing_subscription(id_user):
    subscription = Subscription.query.filter_by(id_user=id_user).first()
    if subscription:
        return jsonify(True)  # Si existe una suscripción para el usuario
    else:
        return jsonify(False)  # Si no existe una suscripción para el usuario
        
# Endpoint para verificar la validez de una suscripción por ID de usuario
@app.route('/subscription/<id_user>/valid', methods=['GET'])
def check_subscription_validity(id_user):
    print("asdasd")
    subscription = Subscription.query.filter_by(id_user=id_user).first()
    if subscription:
        # Verificar si la fecha de vencimiento es mayor o igual a la fecha actual
        current_date = datetime.datetime.now()
        if subscription.end_date >= current_date:
            return jsonify(True)  # La suscripción está vigente
        else:
            return jsonify(False)  # La suscripción ha vencido
    else:
        return jsonify(False)  # No hay suscripción para el usuario