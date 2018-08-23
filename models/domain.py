from db import db


class Domain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String)
    environment = db.Column(db.String)
    domain = db.Column(db.String)

    def __init__(self, customer, environment, domain):
        self.customer = customer
        self.environment = environment
        self.domain = domain

    def json(self):
        return {'Domain': self.domain}

    @classmethod
    def find_by_domain(cls, domain):
        return Domain.query.filter_by(domain=domain).first()

    @classmethod
    def find_by_customer(cls, customer):
        return Domain.query.filter_by(customer=customer).all()

    @classmethod
    def find_all(cls, customer, environment):
        return Domain.query.filter_by(customer=customer, environment=environment)

    @classmethod
    def find_by_environment(cls, environment):
        return Domain.query.filter_by(environment=environment)	

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
