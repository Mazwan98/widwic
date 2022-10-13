from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

# init object dr library
app = Flask(__name__)

# init obj Rest
api = Api(app)

# init obj cors
CORS(app)

# init obj sqlalchemy
db = SQLAlchemy(app)

# Confg DB (utk sementara di Sqlite3)
basedir = os.path.dirname(os.path.abspath(__file__))
database = "sqlite:///" + os.path.join(basedir, "db.sqlite")
app.config["SQLALCHEMY_DATABASE_URI"] = database

# DB Models
class ModelDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100))
    email = db.Column(db.String(50))
    gender = db.Column(db.Integer)

    # mothode nyimpen data biar lebih simple
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except:
            return False

db.create_all()

# init var dict
profil = {}

# class Rest 
class KlasRest(Resource):
    def get(self):
        # tampilkan data dari DB
        query = ModelDB.query.all()

        # iterasi pada ModelDB dengan teknik looping
        output = [
            {
                "id":data.id,
                "nama":data.nama, 
                "email":data.email, 
                "gender":data.gender
            } 
            for data in query
        ]

        response = {
            "code" : 200,
            "msg"  : "Berhasil !",
            "data" : output
        }

        return response, 200

    def post(self):
        dataNama = request.form["nama"]
        dataEmail = request.form["email"]
        dataGender = request.form["gender"]

        # transfer data ke DB
        model = ModelDB(nama=dataNama, email=dataEmail, gender=dataGender)
        model.save()
         
        response = {
            "code" : 200,
            "msg" : "Data telah ditransfer !"
        }

        return response, 200

    # delete all Data
    def delete(self):
        # query all data
        query = ModelDB.query.all() # list comprehentions => looping

        # looping
        for data in query:
            db.session.delete(data)
            db.session.commit()

        response = {
            "code" : 200,
            "msg":"Semua data terhapus !"
        }

        return response, 200
        


# Class Update & Dell
class UpdateData(Resource):
    def put(self, id):
        query = ModelDB.query.get(id) #Berdasarkan ID

        # Form Update
        editNama = request.form["nama"]
        editEmail = request.form["email"]
        editGender = request.form["gender"]

        # Replace nilai
        query.nama = editNama
        query.email = editEmail
        query.gender = editGender
        db.session.commit()

        response = {
            "code" : 200,
            "msg" : "Update data berhasil !"
        }

        return response, 200

    # delete by id
    def delete(self, id):
        queryData = ModelDB.query.get(id)

        # manggil method for delete data by id
        db.session.delete(queryData)
        db.session.commit()

        response = {
            "code" : 200,
            "msg" : "delete data berhasil"
        }
        return response, 200


# init url / api 
# testing
api.add_resource(KlasRest, "/api/", methods=["GET", "POST", "DELETE"])
api.add_resource(UpdateData, "/api/<id>", methods=["PUT", "DELETE"])

if __name__ == "__main__":
    app.run(debug=True, port=2022)
    
