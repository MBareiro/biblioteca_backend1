from app import db, ma, app

class Beneficiary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    
    def __init__(self, name, last_name, phone):
        self.name = name
        self.last_name = last_name
        self.phone = phone

class BeneficiarySchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'last_name', 'phone')

beneficiary_schema = BeneficiarySchema()
beneficiaries_schema = BeneficiarySchema(many=True)

with app.app_context():
    db.create_all()