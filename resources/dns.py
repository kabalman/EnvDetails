from flask import request
from flask_restful import Resource
import psycopg2
from models.dns import DNS


class CreateDNS(Resource):
    def post(self):
        data = request.get_json()
        dnstoadd = DNS(data['customer'], data['environment'], data['dns'])
        try:
            DNS.save_to_db(dnstoadd)
            return {"message": "DNS entry added"}, 201
        except:
            return {'message': 'DNS entry already exists'}, 400


class DeleteDNS(Resource):
    def delete(self, dns):
        dns = DNS.find_by_dns(dns)
        if dns:
            DNS.delete_from_db(dns)
        return {'message': 'DNS entry {} deleted'.format(dns.dns)}


class ListDNS(Resource):
    def get(self, customer, environment):
        try:
            return {'DNSServers': list(map(lambda x: x.json(), DNS.find_all(customer, environment)))}, 200
        except Exception:
            return {'message': 'No DNS entries found'}, 404
			
class ListDNSbyCustomer(Resource):
    def get(self, customer):
        try:
            return {'DNSServers': list(map(lambda x: x.json(), DNS.find_by_customer(customer)))}, 200
        except Exception:
            return {'message': 'No DNS entries found'}, 404
			
class ListDNSbyEnvironment(Resource):
    def get(self, environment):
        try:
            return {'DNSServers': list(map(lambda x: x.json(), DNS.find_by_environment(environment)))}, 200
        except Exception:
            return {'message': 'No DNS entries found'}, 404			
