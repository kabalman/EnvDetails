from db import db


class DNS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String)
    environment = db.Column(db.String)
    dns = db.Column(db.String)

    def __init__(self, customer, environment, dns):
        self.customer = customer
        self.environment = environment
        self.dns = dns

    def json(self):
        return {'DNS': self.dns}

    @classmethod
    def find_by_dns(cls, dns):
        return DNS.query.filter_by(dns=dns).first()

    @classmethod
    def find_by_customer(cls, customer):
        return DNS.query.filter_by(customer=customer).all()

    @classmethod
    def find_all(cls, customer, environment):
        return DNS.query.filter_by(customer=customer, environment=environment)

    @classmethod
    def find_by_environment(cls, environment):
        return DNS.query.filter_by(environment=environment)	

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
