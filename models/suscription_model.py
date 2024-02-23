from app import db, ma, app
from datetime import datetime

class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey('beneficiary.id'), nullable=False)

    def __init__(self, start_date, end_date, id_user):
        self.start_date = start_date
        self.end_date = end_date
        self.id_user = id_user

class SubscriptionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'start_date', 'end_date', 'id_user')

subscription_schema = SubscriptionSchema()
subscriptions_schema = SubscriptionSchema(many=True)

with app.app_context():
    db.create_all()
