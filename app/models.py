from autoapp import db
from sqlalchemy.inspection import inspect

"""
Contains the data model for each credit policies. Each credit policies contain following variables in the JSON format
customer_income     :(int) Monthly income of the customer.
customer_debt       :(int) Existing debt of the customer.
payment_remarks_12m :(int) Payment remarks (12m) of the customer. 
payment_remarks     :(int) Payment remarks of the customer.
customer_age        :(int) Age of the customer. 
"""

class Serializer(object):
    """
    Converts SQLAlhemy Model to JSON
    """
    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]


class CreditPolicies(db.Model, Serializer):
    __tablename__ = 'Credit Policies'
    policy_id           = db.Column(db.Integer, primary_key=True)
    customer_income     = db.Column(db.Integer, nullable=False)
    customer_debt       = db.Column(db.Integer, nullable=False)
    payment_remarks_12m = db.Column(db.Integer, nullable=False)
    payment_remarks     = db.Column(db.Integer, nullable=False)
    customer_age        = db.Column(db.Integer, nullable=False)

    def __init__(self, customer_income, customer_debt, payment_remarks_12m, payment_remarks, customer_age):
        self.customer_income = customer_income
        self.customer_debt = customer_debt
        self.payment_remarks_12m = payment_remarks_12m
        self.payment_remarks = payment_remarks
        self.customer_age = customer_age

    def serialize(self):
        deserial = Serializer.serialize(self)
        return deserial

    def __repr__(self):
        return f"Credit Policy (Customer Income = {self.customer_income}, Customer Debt = {self.customer_debt},\
                                Payment Remark 12m = {self.payment_remark_12m}, Payment Remark = {self.payment_remark},\
                                Customer Age = {self.customer_age})"