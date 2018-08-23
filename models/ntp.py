from db import db


class NTP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String)
    environment = db.Column(db.String)
    ntp = db.Column(db.String)

    def __init__(self, customer, environment, ntp):
        self.customer = customer
        self.environment = environment
        self.ntp = ntp

    def json(self):
        return {'NTP': self.ntp}

    @classmethod
    def find_by_ntp(cls, ntp):
        return NTP.query.filter_by(ntp=ntp).first()

    @classmethod
    def find_by_customer(cls, customer):
        return NTP.query.filter_by(customer=customer).all()

    @classmethod
    def find_all(cls, customer, environment):
        return NTP.query.filter_by(customer=customer, environment=environment)

    @classmethod
    def find_by_environment(cls, environment):
        return NTP.query.filter_by(environment=environment)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
