from flask import Flask, jsonify, request
from playhouse.shortcuts import model_to_dict, dict_to_model
from peewee import *


db = PostgresqlDatabase('contacts', user='',
                        password='', host='localhost', port=5432)


class BaseModel(Model):
    class Meta:
        database = db


class Contact(BaseModel):
    name = CharField()
    phone_number = BigIntegerField()


db.connect()
db.drop_tables([Contact])
db.create_tables([Contact])


Contact(name='Luis', phone_number=6462033499).save()
Contact(name='rafi', phone_number=7182348888).save()

app = Flask(__name__)


@app.route('/')
def index():
    return "API ROOT"


@app.route('/contact/', methods=['GET', 'POST'])
@app.route('/contact/<id>', methods=['GET', 'PUT', 'DELETE'])
def endpoint(id=None):
    if request.method == 'GET':
        if id:
            return jsonify(model_to_dict(Contact.get(Contact.id == id)))
        else:
            staff = []
            for employee in Contact.select():
                staff.append(model_to_dict(employee))
            return jsonify(staff)

    if request.method == 'PUT':
        body = request.get_json()
        Contact.update(body).where(Contact.id == id).execute()
        return "Contact " + str(id) + " has been updated."

    if request.method == 'POST':
        new_employee = dict_to_model(Contact, request.get_json())
        new_employee.save()
        return jsonify({"success": True})

    if request.method == 'DELETE':
        Contact.delete().where(Contact.id == id).execute()
        return "Contact " + str(id) + " deleted."


app.run(port=5000, debug=True)
