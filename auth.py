from flask import Flask, request, make_response, jsonify
from flask_restful import Resource, Api
import jwt 
import datetime 

# lib utk build decorator
from functools import wraps

app = Flask(__name__) # Flask
api = Api(app) # Rest
app.config['SECRET_KEY'] = "rahasia"

# decorator kunci endpoint / auth
def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs): # arguments & key arguments
        # token akan diparsing melalui parameter dari endpoint
        token = request.args.get('token')

        # Looping cek token
        if not token:
            return make_response(jsonify({"msg":"token kosong bro !"}), 404) # Not Found

        # decode token yang diterima 
        try:
            output = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return make_response(jsonify({"msg":"token Salah / invalid !"}))
        return f(*args, **kwargs)  # arguments & key arguments
    return decorator 


# Build endpoint utk login
class Login(Resource):
    def post(self):
        # butuh multipat form utk transmisi data
        username = request.form.get('username')
        password = request.form.get('password')

        # membuat kondisi pengecekan Password 
        if username and password == 'superadmin':
            # menghasilkan nomor token
            token = jwt.encode(
                {
                    "username": username, 
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=5) # exp: 5 Menit
                },
                app.config['SECRET_KEY'], algorithm="HS256"
            )
            return jsonify({
                "token":token,
                "msg": "Anda berhasil Masuk !"
            })
        
        return jsonify({"msg": "Login dulu !"})

# Page protected 
class Dashboard(Resource):
    # nambah decorator utk mengunci
    @token_required
    def get(self):
        return jsonify({"msg":"Halaman Dashboard"})


# Page not-protected
class HomePage(Resource):
    def get(self):
        return jsonify({"msg":"Halaman umum"})

api.add_resource(Login, "/api/login", methods=["POST"])
api.add_resource(Dashboard, "/api/dashboard", methods=["GET"])
api.add_resource(HomePage, "/api", methods=["GET"])

if __name__ == "__main__":
    app.run(debug=True, port=2022)