from flask import request
from flask_restful import Resource
import psycopg2
from models.ntp import NTP


class CreateNTP(Resource):
    def post(self):
        data = request.get_json()
        ntptoadd = NTP(data['customer'], data['environment'], data['ntp'])
        try:
            NTP.save_to_db(ntptoadd)
            return {"message": "NTP entry added"}, 201
        except:
            return {'message': 'NTP entry already exists'}, 400


class DeleteNTP(Resource):
    def delete(self, ntp):
        ntp = NTP.find_by_ntp(ntp)
        if ntp:
            NTP.delete_from_db(ntp)
        return {'message': 'NTP entry {} deleted'.format(ntp.ntp)}


class ListNTP(Resource):
    def get(self, customer, environment):
        try:
            return {'NTPServers': list(map(lambda x: x.json(), NTP.find_all(customer, environment)))}, 200
        except Exception:
            return {'message': 'No NTP entries found'}, 404
			
class ListNTPbyCustomer(Resource):
    def get(self, customer):
        try:
            return {'NTPServers': list(map(lambda x: x.json(), NTP.find_by_customer(customer)))}, 200
        except Exception:
            return {'message': 'No NTP entries found'}, 404
			
class ListNTPbyEnvironment(Resource):
    def get(self, environment):
        try:
            return {'NTPServers': list(map(lambda x: x.json(), NTP.find_by_environment(environment)))}, 200
        except Exception:
            return {'message': 'No NTP entries found'}, 404			
