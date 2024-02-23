from app import db, ma, app

class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    loan_date = db.Column(db.Date, nullable=True)
    return_date = db.Column(db.Date, nullable=True)
    returned = db.Column(db.Boolean, nullable=True)
    beneficiaries_id = db.Column(db.Integer, nullable=False)
    books_id = db.Column(db.Integer, nullable=False)

    def __init__(self, loan_date, return_date, returned, beneficiaries_id, books_id):
        self.loan_date = loan_date
        self.return_date = return_date
        self.returned = returned
        self.beneficiaries_id = beneficiaries_id
        self.books_id = books_id

class LoanSchema(ma.Schema):
    class Meta:
        fields = ('id', 'loan_date', 'return_date', 'returned', 'beneficiaries_id', 'books_id')

loan_schema = LoanSchema()
loans_schema = LoanSchema(many=True)

with app.app_context():
    db.create_all()
