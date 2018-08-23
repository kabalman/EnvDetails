from flask import request
from flask_restful import Resource
import psycopg2
from models.domain import Domain


class CreateDomain(Resource):
    def post(self):
        data = request.get_json()
        domaintoadd = Domain(data['customer'], data['environment'], data['domain'])
        try:
            Domain.save_to_db(domaintoadd)
            return {"message": "Domain entry added"}, 201
        except:
            return {'message': 'Domain entry already exists'}, 400


class DeleteDomain(Resource):
    def delete(self, domain):
        domain = Domain.find_by_domain(domain)
        if domain:
            Domain.delete_from_db(domain)
        return {'message': 'Domain entry {} deleted'.format(domain.domain)}


class ListDomain(Resource):
    def get(self, customer, environment):
        try:
            return {'Domains': list(map(lambda x: x.json(), Domain.find_all(customer, environment)))}, 200
        except Exception:
            return {'message': 'No Domain entries found'}, 404
			
class ListDomainbyCustomer(Resource):
    def get(self, customer):
        try:
            return {'Domains': list(map(lambda x: x.json(), Domain.find_by_customer(customer)))}, 200
        except Exception:
            return {'message': 'No Domain entries found'}, 404
			
class ListDomainbyEnvironment(Resource):
    def get(self, environment):
        try:
            return {'Domains': list(map(lambda x: x.json(), Domain.find_by_environment(environment)))}, 200
        except Exception:
            return {'message': 'No Domain entries found'}, 404			
