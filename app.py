from flask import Flask, render_template, request, session, make_response, flash, url_for, redirect
import requests
from flask_restful import Api
import os
from resources.dns import CreateDNS, DeleteDNS, ListDNS, ListDNSbyCustomer, ListDNSbyEnvironment
from resources.ntp import CreateNTP, DeleteNTP, ListNTP, ListNTPbyCustomer, ListNTPbyEnvironment
from resources.domain import CreateDomain, DeleteDomain, ListDomain, ListDomainbyCustomer, ListDomainbyEnvironment
from models.user import User
from models.dns import DNS
from models.ntp import NTP
from models.domain import Domain
import io
import csv


connectionstring = "postgresql://" + os.environ.get('PG_USER') + ":" + os.environ.get('PG_PASSWORD') + "@" + os.environ.get('PG_HOST') + "/" + os.environ.get('PG_DATABASE')

app = Flask(__name__)
app.secret_key = "uV77gcmxmSrQXwiHV7xM"

api = Api(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = connectionstring

# creates all of the tables before the first api call
@app.before_first_request
def create_tables():
    db.create_all()

# ----------------------------------------------------------------------------------
#           API APPLICATION
# ----------------------------------------------------------------------------------

# DNS
api.add_resource(CreateDNS, '/api/dns/create')
api.add_resource(DeleteDNS, '/api/dns/delete/<string:dns>')
api.add_resource(ListDNS, '/api/dns/list/<string:customer>/<string:environment>')
api.add_resource(ListDNSbyCustomer, '/api/dns/listbycust/<string:customer>')
api.add_resource(ListDNSbyEnvironment, '/api/dns/listbyenv/<string:environment>')

# NTP
api.add_resource(CreateNTP, '/api/ntp/create')
api.add_resource(DeleteNTP, '/api/ntp/delete/<string:dns>')
api.add_resource(ListNTP, '/api/ntp/list/<string:customer>/<string:environment>')
api.add_resource(ListNTPbyCustomer, '/api/ntp/listbycust/<string:customer>')
api.add_resource(ListNTPbyEnvironment, '/api/ntp/listbyenv/<string:environment>')

# Customer Domains
api.add_resource(CreateDomain, '/api/domain/create')
api.add_resource(DeleteDomain, '/api/domain/delete/<string:dns>')
api.add_resource(ListDomain, '/api/domain/list/<string:customer>/<string:environment>')
api.add_resource(ListDomainbyCustomer, '/api/domain/listbycust/<string:customer>')
api.add_resource(ListDomainbyEnvironment, '/api/domain/listbyenv/<string:environment>')

# ----------------------------------------------------------------------------------
#           WEB APPLICATION
# ----------------------------------------------------------------------------------

# login page
@app.route("/")
def root():
    User.logout()
    return render_template('login.html')


# Login page (home page)
@app.route("/login", methods=['POST', 'GET'])
def login_user():
    if request.method == 'GET':
        User.logout()
        return render_template('login.html')
    else:
        email = request.form['email']
        password = request.form['password']
        # Checks if the users login credentials are vaild if not it returns them to the login screen
        if User.login_valid(email, password):
            User.login(email)
        else:
            session['email'] = None
            error = 'Invalid credentials'
            return render_template('login.html', error=error)
        # If login details are correct the user is forwarded to their profile page
        return redirect(url_for('profile'))

# Profile page (user is directed to this page after login)
@app.route("/profile")
def profile():
    return render_template('profile.html', email=session['email'])

# This page allows you to add new users to be able to login and use the tool - this is hidden from the web page
# There should be a logged in user to access this page
@app.route("/user-add", methods=['POST', 'GET'])
def usercreate():
    if request.method == 'GET':
        if session['email'] is not None:
            return render_template('user.html')
        else:
            return render_template('login.html')
#            return render_template('user.html')
    else:
        email = request.form['email']
        password = request.form['password']
        customer = request.form['customer']
        if User.create_user(email, password, customer):
            flash('User added successfully')
            return render_template('user.html')
        else:
            error = 'Failed to add user'
            return render_template('user.html', error=error)

# -------------
# DNS SERVICES
# -------------
@app.route("/dns/add", methods=['POST', 'GET'])
def dnscreate():
    # This gets the customer that the user was assigned to and sets that as a static value in the application so they can only create DNS server entries for their customer
    user = User.get_by_email(session['email'])
    customer = user.customer

    if request.method == 'GET':
        return render_template('dns.html', email=session['email'], customer=customer)
    else:
        # This sets variables based on what the user enters into the web form
        environment = request.form['environment']
        dns = request.form['dns']

        # This is the message data being collected to be passed as part of the api call
        message_data = {}
        message_data['customer'] = customer
        message_data['environment'] = environment
        message_data['dns'] = dns

        msg_headers = {
            'Content-Type': 'application/json'
        }
        url = 'http://localhost:5000/api/dns/create'
        print("Message data: {}".format(message_data))
        # runs the api call to create a new DNS server entry
        r = requests.post(url, json=message_data, headers=msg_headers, verify=False)
        if r.status_code == 201:
            flash('DNS Server entry added successfully')
            return render_template('dns.html', customer=customer)
        elif r.status_code == 400:
            error = 'DNS server entry already exists'
            return render_template('dns.html', error=error, customer=customer)
        else:
            error = 'Unknown Error Occured'
            return render_template('dns.html', error=error, customer=customer)


@app.route("/dns/list")
def dnslist():
    # Gets the customer the user is assigned to and shows all of the DNS server entries for that customer
    user = User.get_by_email(session['email'])
    customer = user.customer
    entries = DNS.find_by_customer(customer)
    return render_template('listdns.html', entries=entries)


@app.route("/dns/export")
def dnsexport():
    # Exports all of the DNS entries for the users customer into a csv file that the user can download
    user = User.get_by_email(session['email'])
    customer = user.customer
    q = DNS.find_by_customer(customer)
    csv_list = [['Customer', 'Environment', 'DNS Server']]
    for each in q:
        csv_list.append(
            [
                each.customer,
                each.environment,
                each.dns
            ]
        )
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerows(csv_list)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output

# -------------
# NTP SERVICES
# -------------
@app.route("/ntp/add", methods=['POST', 'GET'])
def ntpcreate():
    # This gets the customer that the user was assigned to and sets that as a static value in the application so they can only create NTP server entries for their customer
    user = User.get_by_email(session['email'])
    customer = user.customer

    if request.method == 'GET':
        return render_template('ntp.html', email=session['email'], customer=customer)
    else:
        # This sets variables based on what the user enters into the web form
        environment = request.form['environment']
        ntp = request.form['ntp']

        # This is the message data being collected to be passed as part of the api call
        message_data = {}
        message_data['customer'] = customer
        message_data['environment'] = environment
        message_data['ntp'] = ntp

        msg_headers = {
            'Content-Type': 'application/json'
        }
        url = 'http://localhost:5000/api/ntp/create'
        print("Message data: {}".format(message_data))
        # runs the api call to create a new NTP server entry
        r = requests.post(url, json=message_data, headers=msg_headers, verify=False)
        if r.status_code == 201:
            flash('NTP Server entry added successfully')
            return render_template('ntp.html', customer=customer)
        elif r.status_code == 400:
            error = 'NTP server entry already exists'
            return render_template('ntp.html', error=error, customer=customer)
        else:
            error = 'Unknown Error Occured'
            return render_template('ntp.html', error=error, customer=customer)


@app.route("/ntp/list")
def ntplist():
    # Gets the customer the user is assigned to and shows all of the NTP server entries for that customer
    user = User.get_by_email(session['email'])
    customer = user.customer
    entries = NTP.find_by_customer(customer)
    return render_template('listntp.html', entries=entries)


@app.route("/ntp/export")
def ntpexport():
    # Exports all of the NTP entries for the users customer into a csv file that the user can download
    user = User.get_by_email(session['email'])
    customer = user.customer
    q = NTP.find_by_customer(customer)
    csv_list = [['Customer', 'Environment', 'NTP Server']]
    for each in q:
        csv_list.append(
            [
                each.customer,
                each.environment,
                each.ntp
            ]
        )
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerows(csv_list)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output

# -------------------------
# CUSTOMER DOMAIN SERVICES
# -------------------------
@app.route("/domain/add", methods=['POST', 'GET'])
def domaincreate():
    # This gets the customer that the user was assigned to and sets that as a static value in the application so they can only create Domain server entries for their customer
    user = User.get_by_email(session['email'])
    customer = user.customer

    if request.method == 'GET':
        return render_template('domain.html', email=session['email'], customer=customer)
    else:
        # This sets variables based on what the user enters into the web form
        environment = request.form['environment']
        domain = request.form['domain']

        # This is the message data being collected to be passed as part of the api call
        message_data = {}
        message_data['customer'] = customer
        message_data['environment'] = environment
        message_data['domain'] = domain

        msg_headers = {
            'Content-Type': 'application/json'
        }
        url = 'http://localhost:5000/api/domain/create'
        print("Message data: {}".format(message_data))
        # runs the api call to create a new Domain server entry
        r = requests.post(url, json=message_data, headers=msg_headers, verify=False)
        if r.status_code == 201:
            flash('Customer Domain entry added successfully')
            return render_template('domain.html', customer=customer)
        elif r.status_code == 400:
            error = 'Customer Domain entry already exists'
            return render_template('domain.html', error=error, customer=customer)
        else:
            error = 'Unknown Error Occured'
            return render_template('domain.html', error=error, customer=customer)


@app.route("/domain/list")
def domainlist():
    # Gets the customer the user is assigned to and shows all of the Domain server entries for that customer
    user = User.get_by_email(session['email'])
    customer = user.customer
    entries = Domain.find_by_customer(customer)
    return render_template('listdomain.html', entries=entries)


@app.route("/domain/export")
def domainexport():
    # Exports all of the Domain entries for the users customer into a csv file that the user can download
    user = User.get_by_email(session['email'])
    customer = user.customer
    q = Domain.find_by_customer(customer)
    csv_list = [['Customer', 'Environment', 'Domain']]
    for each in q:
        csv_list.append(
            [
                each.customer,
                each.environment,
                each.domain
            ]
        )
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerows(csv_list)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output

if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(host='0.0.0.0', port=5000)
