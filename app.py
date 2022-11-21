from flask import Flask, jsonify, request
from playhouse.shortcuts import model_to_dict, dict_to_model
from peewee import *

app=Flask(__name__)



db=PostgresqlDatabase('contacts',user='postgres',password='',host='localhost',port=5432)

class BaseModel(Model):
  class Meta:
    database=db

class Contact(BaseModel):
  name=CharField()
  phone_number=IntegerField()

db.connect()
db.drop_tables([Contact])
db.create_tables([Contact])


Contact(name='Luis', phone_number=1233).save()
Contact(name='rafi',phone_number=12344).save()

app.run(port=5000,debug=True)


