import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017')

mydb = client['employee']

information = mydb.employeeInformations