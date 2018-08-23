# Environment Details REST Api

This is built with Flask, Flask-RESTful, Flask-SQLAlchemy, psycopg2

This application provides a RESTful webservice (API) can be used to create, list and delete the following:

- DNS servers by Customer and Environment e.g. DNS servers relating to customer EON environment Development
- NTP servers by Customer and Environment
- Customer Domains by Customer and Environment

The application also provides a user interface that can be used to add/list DNS servers, NTP servers and Customer domains by customer and environment.

## DNS Services
###### Create a DNS server entry in the application's database
curl --header "Content-Type: application/json" --request POST --data '{"dns":"<string:dns>","customer":"<string:customer>","environment": "<string:environment>"}' http://<URL>/api/dns/create
###### Delete a DNS server entry in the application's database
curl --header "Content-Type: application/json" --request DELETE http://<URL>/api/dns/delete/<string:dns>
###### List all DNS server entries for the Customer and Environment
curl --header "Content-Type: application/json"  -request GET http://<URL>/api/dns/list/<string:customer>/<string:environment>
###### List all DNS entries for the Customer
curl --header "Content-Type: application/json"  -request GET http://<URL>/api/dns/listbycust/<string:customer>
###### List all DNS entries for the Environment
curl --header "Content-Type: application/json"  -request GET http://<URL>/api/dns/listbyenv/<string:environment>

## NTP Services
###### Create a NTP server entry in the application's database
curl --header "Content-Type: application/json" --request POST --data '{"ntp":"<string:ntp>","customer":"<string:customer>","environment": "<string:environment>"}' http://<URL>/api/ntp/create
###### Delete a NTP server entry in the application's database
curl --header "Content-Type: application/json" --request DELETE http://<URL>/api/ntp/delete/<string:ntp>
###### List all NTP server entries for the Customer and Environment
curl --header "Content-Type: application/json"  -request GET http://<URL>/api/ntp/list/<string:customer>/<string:environment>
###### List all NTP entries for the Customer
curl --header "Content-Type: application/json"  -request GET http://<URL>/api/ntp/listbycust/<string:customer>
###### List all NTP entries for the Environment
curl --header "Content-Type: application/json"  -request GET http://<URL>/api/ntp/listbyenv/<string:environment>

## Domain Services
###### Create a Domain server entry in the application's database
curl --header "Content-Type: application/json" --request POST --data '{"domain":"<string:domain>","customer":"<string:customer>","environment": "<string:environment>"}' http://<URL>/api/domain/create
###### Delete a Domain server entry in the application's database
curl --header "Content-Type: application/json" --request DELETE http://<URL>/api/domain/delete/<string:domain>
###### List all Domain server entries for the Customer and Environment
curl --header "Content-Type: application/json"  -request GET http://<URL>/api/domain/list/<string:customer>/<string:environment>
###### List all Domain entries for the Customer
curl --header "Content-Type: application/json"  -request GET http://<URL>/api/domain/listbycust/<string:customer>
###### List all Domain entries for the Environment
curl --header "Content-Type: application/json"  -request GET http://<URL>/api/domain/listbyenv/<string:environment>

## User Interface
The application also provides a UI to add/list the following:
- DNS servers by Customer and Environment e.g. DNS servers relating to customer EON environment Development
- NTP servers by Customer and Environment
- Customer Domains by Customer and Environment

The UI can be accessed on http://<URL>
