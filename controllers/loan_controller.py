from flask import jsonify, request
from app import app, db
from models.loan_model import Loan, LoanSchema
from models.beneficiary_model import Beneficiary
from models.book_model import Book

loan_schema = LoanSchema()
loans_schema = LoanSchema(many=True)

@app.route('/loans', methods=['GET'])
def get_loans():
    print("aaaaaaa")
    try:
        all_loans = Loan.query.all()

        # Lista para almacenar resultados con nombres de libro y beneficiario
        loans_with_names = []

        for loan in all_loans:
            # Consulta para obtener el nombre del beneficiario
            beneficiary = Beneficiary.query.get(loan.beneficiaries_id)
            beneficiary_name = beneficiary.name if beneficiary else "Beneficiary not found"

            # Consulta para obtener el nombre del beneficiario
            beneficiary = Beneficiary.query.get(loan.beneficiaries_id)
            beneficiary_last_name = beneficiary.last_name if beneficiary else "Beneficiary not found"

            # Consulta para obtener el título del libro
            book = Book.query.get(loan.books_id)
            book_title = book.title if book else "Book not found"

            # Convierte el objeto Loan a un diccionario
            loan_dict = loan_schema.dump(loan)

            # Agrega los nombres del libro y beneficiario al diccionario
            loan_dict['beneficiaryName'] = beneficiary_name
            loan_dict['beneficiary_last_name'] = beneficiary_last_name
            loan_dict['bookTitle'] = book_title

            # Agrega el diccionario a la lista
            loans_with_names.append(loan_dict)

        return jsonify(loans_with_names)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Get a loan by its ID
@app.route('/loans/<id>', methods=['GET'])
def get_loan(id):
    loan = Loan.query.get(id)
    return loan_schema.jsonify(loan)

""" # Delete a loan by its ID
@app.route('/loans/<id>', methods=['DELETE'])
def delete_loan(id):
    loan = Loan.query.get(id)
    if loan:
        db.session.delete(loan)
        db.session.commit()
        return loan_schema.jsonify(loan)
    else:
        return jsonify({'message': 'Loan not found'}), 404
 """

# Create a new loan
@app.route('/loans', methods=['POST'])
def create_loan():
    loan_date = request.json['loan_date']
    return_date = request.json['return_date']
    returned = request.json['returned']
    beneficiaries_id = request.json['beneficiaries_id']
    books_id = request.json['books_id']

    # Crear nuevo préstamo
    new_loan = Loan(
        loan_date=loan_date,
        return_date=return_date,
        returned=returned,
        beneficiaries_id=beneficiaries_id,
        books_id=books_id
    )

    # Actualizar disponibilidad del libro
    book = Book.query.get(books_id)
    if book:
        book.available -= 1  # Restarle 1 al campo 'available' del libro
        db.session.commit()    

    # Guardar el nuevo préstamo
    db.session.add(new_loan)
    db.session.commit()

    return loan_schema.jsonify(new_loan)


# Update a loan by its ID
@app.route('/loans/<id>', methods=['PUT'])
def update_loan(id):
    loan = Loan.query.get(id)
    if loan is None:
        return jsonify({'message': 'Loan not found'}), 404

    loan.loan_date = request.json['loan_date']
    loan.return_date = request.json['return_date']
    loan.returned = request.json['returned']
    loan.beneficiaries_id = request.json['beneficiaries_id']
    loan.books_id = request.json['books_id']

    db.session.commit()
    return loan_schema.jsonify(loan)

# Delete a loan by its ID
@app.route('/loan-cancel/<id>', methods=['PUT'])
def cancel_loan(id):
    print("CABCEL")
    loan = Loan.query.get(id)
    if loan is None:
        return jsonify({'message': 'Loan not found'}), 404

    loan.returned = True  # Establecer el estado de cancelación en True
    db.session.commit()
    # Incrementar el número de libros disponibles
    book = Book.query.get(loan.books_id)
    if book:
        book.available += 1
        db.session.commit()
    return loan_schema.jsonify(loan)
