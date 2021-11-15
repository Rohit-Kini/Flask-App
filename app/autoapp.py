from flask import Flask, request
from flask_restful import Api, Resource, abort, reqparse, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.inspection import inspect
from models import *

"""
Initializing Flask Web App and database
"""
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Anyfin-Rohit-Kini'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///policy_database.db'
api = Api(app)
db = SQLAlchemy(app)

"""
Request Argument Parsers : Parsing arguments to the HTML methods
Two - Kind of Argument Parser
a) PUT      - Arguments to parse to PUT method 
b) PATCH    - Arguments to parse to PATCH method
"""
policy_put_args = reqparse.RequestParser()
policy_put_args.add_argument("customer_income", type=int, help="Monthly Customer's Income Required.", required=True)
policy_put_args.add_argument("customer_debt", type=int, help="Customer's Existing Debt Required.", required=True)
policy_put_args.add_argument("payment_remarks_12m", type=int, help="Customer's Payment Remarks (12m) Required.", required=True)
policy_put_args.add_argument("payment_remarks", type=int, help="Customer's Payment Remarks Required.", required=True)
policy_put_args.add_argument("customer_age", type=int, help="Customer's Age Required.", required=True)

policy_patch_args = reqparse.RequestParser()
policy_patch_args.add_argument("customer_income", type=int, help="Monthly Customer's Income.", required=False)
policy_patch_args.add_argument("customer_debt", type=int, help="Customer's Existing Debt.", required=False)
policy_patch_args.add_argument("payment_remarks_12m", type=int, help="Customer's Payment Remarks (12m).", required=False)
policy_patch_args.add_argument("payment_remarks", type=int, help="Customer's Payment Remarks.", required=False)
policy_patch_args.add_argument("customer_age", type=int, help="Customer's Age.", required=False)

resorce_fields = {
    "policy_id" : fields.Integer,
    "customer_income": fields.Integer,
    "customer_debt": fields.Integer,
    "payment_remarks_12m": fields.Integer,
    "payment_remarks": fields.Integer,
    "customer_age": fields.Integer
}

"""
Function to check if the given policy should be accepted/rejected
"""
def _check(policy):
    isValid = True
    reason =  []
    income_check = (policy['customer_income']<500)
    debt_check = (policy['customer_debt'] > 0.5*policy['customer_income'])
    payment_remarks_12m_check = (policy['payment_remarks_12m'] > 0)
    payment_remarks_check = (policy['payment_remarks'] > 1)
    age_check = (policy['customer_age'] < 18)
    
    if income_check:
        isValid = False
        reason.append('LOW_INCOME')
    if debt_check:
        isValid = False
        reason.append('HIGH_DEBT_FOR_INCOME')
    if payment_remarks_12m_check:
        isValid = False
        reason.append('PAYMENT_REMARKS_12M')
    if payment_remarks_check:
        isValid = False
        reason.append('PAYMENT_REMARKS')
    if age_check:
        isValid = False
        reason.append('UNDERAGE')
    return isValid, reason

class Policy(Resource):
    """
    Methods:
    ------------------------------------------------------------------
    Endpoint /policy/<int>policy_id

    GET     - get the existing policy (if stored in database).
    PUT     - put a new policy to the database.
    PATCH   - update the existing policy or attributes of the policy.
    DELETE  - delete the policy (if exists in database).
    POST    - validate the current policy - either ACCEPT or REJECT. 
    
    Endpoint /checkpolicy

    POST    - validate the policy given as a input.
    """

    @marshal_with(resorce_fields)   
    def get(self, policy_id):
        result = CreditPolicies.query.filter_by(policy_id=policy_id).first()
        if not result:
            abort(404, message="Could not find the policy with that ID")
        return result

    @marshal_with(resorce_fields)
    def put(self, policy_id):
        args = policy_put_args.parse_args()
        result = CreditPolicies.query.filter_by(policy_id=policy_id).first()
        if result:
            abort(409, message="Policy ID already taken...")
        CreditP = CreditPolicies(customer_income=args['customer_income'], customer_debt=args['customer_debt'],\
                                payment_remarks_12m=args['payment_remarks_12m'], payment_remarks=args['payment_remarks'],\
                                customer_age=args['customer_age'])
        db.session.add(CreditP)
        db.session.commit()
        return CreditP, 201

    @marshal_with(resorce_fields)
    def patch(self, policy_id):
        args = policy_patch_args.parse_args()
        result = CreditPolicies.query.filter_by(policy_id=policy_id).first()
        if not result:
            abort(404, message ="Policy requested doesnot exist, cannot update")
        if args['customer_income']:
            result.customer_income = args['customer_income']
        if args['customer_debt']:
            result.customer_debt = args['customer_debt']
        if args['payment_remarks_12m']:
            result.payment_remarks_12m = args['payment_remarks_12m']
        if args['payment_remarks']:
            result.payment_remarks = args['payment_remarks']
        if args['customer_age']:
            result.customer_age = args['customer_age']
        db.session.commit()
        return result
    
    def post(self, policy_id):
        result = CreditPolicies.query.filter_by(policy_id=policy_id).first()
        if not result:
            abort(404, message = "Policy requested doesnont exist, cannot check")
        policy = result.serialize()
        isValid, reason = _check(policy)
        if isValid:
            return {"Policy" : "ACCEPT", "Reason": "All conditions passed"}
        else:
            return {"Policy" : "REJECT", "Reason/(s)" : reason} 

    def delete(self, policy_id):
        result = CreditPolicies.query.filter_by(policy_id=policy_id).first() 
        if not result:
            abort(404, message = "Nothing to delete")
        db.session.delete(result)
        db.session.commit()
        return  '', 204

class checkPolicy(Resource):
    def post(self):
        if request.is_json:
            policy = request.get_json()
            isValid, reason = _check(policy)
            if isValid:
                return {"Policy" : "ACCEPT", "Reason": "All conditions passed"}
            else:
                return {"Policy" : "REJECT", "Reason/(s)" : reason} 
        return {"Error" : "Request must be JSON"}, 415

api.add_resource(Policy, "/policy/<int:policy_id>")
api.add_resource(checkPolicy, "/checkpolicy")

if __name__ == '__main__':
    app.run(debug=True)