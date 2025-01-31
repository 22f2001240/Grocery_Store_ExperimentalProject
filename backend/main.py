from flask import Flask,request
import os
from flask_restful import Api,Resource
from applications.model import db,Users
from applications.api import *
from applications.auth_api import *
from applications.category_api import *
from applications.product_api import *
from applications.purchase_api import *
from flask_jwt_extended import JWTManager
from datetime import timedelta


base_dir = os.path.abspath(os.path.dirname(__file__)) #To mention the path which i want to store the db instead of storing it in instances folder by def.
#instead of creating db inside a instance folder, we are directly creating the db file in the folder which we are running the app.py file


#create an app instance (variable to assign app)
app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///" +os.path.join(base_dir,"grocery_storedb.sqlite3")
#app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///grocery_storedb.sqlite3"
app.config['SECRET_KEY'] = 'groceryapp123'
app.config['JWT_SECRET_KEY'] = 'grocery123'
app.config['JWT_ACCESS_TOKEN_EXPIRES']=timedelta(hours=12)  

#registering db instance with the app itself and push the current context to the app
db.init_app(app) 
api=Api(app)
jwt=JWTManager(app) #flask security
app.app_context().push() 

def add_admin():
    admin=Users.query.filter_by(role='admin').first()
    if not admin:
        admin=Users(id=1,email_id='admin@gmail.com',password='admin',name='Admin',role='admin')
        db.session.add(admin)
        db.session.commit()
        return "Admin added"
    else:
        return "admin is there"

api.add_resource(WelcomeAPI,'/api/welcome')
api.add_resource(LoginAPI,'/api/login','/api/approve/<int:manager_id>')
api.add_resource(SignupAPI,'/api/signup')
api.add_resource(CategoryAPI,'/api/category','/api/category/<int:category_id>')
api.add_resource(ProductAPI,'/api/product','/api/product/<int:product_id>')

if __name__=='__main__':
    db.create_all()
    add_admin()
    app.run(debug=True)



#thunder client is used to test api (api testing tool)
#cannot have a method in a single class twice or more
#In class based api we cannot use custom function naame . should write the function name as methods
#flask, flask_restful redis,celery,flask_cors,flask_caching,flask_jwt_extended,flask_sqlalchemy