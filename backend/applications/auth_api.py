from flask import Flask,request,current_app as app,flash,jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity,get_jwt #using JWT for the security
from .model import *
import re
from functools import wraps

#200-okey , 201-create a new record,404-not found, 400-bad request, 401-authentication issue, 403 auth, 405-method not found

def roles_required(allowed_roles): #Authorization RBAC-Role Based Access Control
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args,**kwargs):
            if get_jwt().get("role") not in allowed_roles:
                return {"message":"Access denied!"},403
            return fn(*args,**kwargs)
        return wrapper
    return decorator

class LoginAPI(Resource):
    def post(self):
        data=request.json
        email = data.get("email_id").strip()
        password = data.get("password").strip()

        if not email or not password:
            return {'message': 'Email and password are required!'}, 400

        user=Users.query.filter_by(email_id=email,password=password).first()
        if user:
            if user.password == data.get('password'):
                if user.role=='manager' and user.status=='pending':
                    return {'message':'Sorry you are not verified yet!!'}
                access_token=create_access_token(identity=user.id,additional_claims={"role": user.role})
                return {'message':'User logged in successfully',"token":access_token},200
            return {'message':"Incorrect Password"},400
        
        return {'message':"User not found"},404
    
    @jwt_required()
    @roles_required(['admin'])
    def patch(self,manager_id): #To approve managers (temp)
        manager=Users.query.get(manager_id)
        if not manager:
            return {'message':'Manager does not exist'},404
        manager.status='active'
        db.session.commit()
        return {'message':'Manager approved successfuly'},200

class SignupAPI(Resource):  #login and signup use post method. but for single class can only use one post
    def post(self):
        data=request.json
        # Check if all required fields are provided
        required_fields = ['email_id', 'password', 'name', 'role']
        if not all(field in data and data[field].strip() for field in required_fields):
            return {'message': 'Bad request! All fields are required.'}, 400

        email = data.get('email_id').strip()
        password = data.get('password').strip()
        role = data.get('role').strip()

        # Email validation (Regex)
        email_regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
        if not re.match(email_regex, email):
            return {'message': 'Invalid email format!'}, 400

        # Password length validation (Max 10 characters)
        if len(password) > 10 or len(password) < 3:
            return {'message': 'Password must be at most 10 characters and atleast 3 characters long!'}, 400
        
        # Role validation (Only "customer" or "manager" allowed)
        allowed_roles = {"customer", "manager"}
        if role not in allowed_roles:
            return {'message': "Invalid role! Role must be either 'customer' or 'manager'."}, 400
        
        # Check if user already exists
        user = Users.query.filter_by(email_id=email).first()
        if user:
            return {'message': 'User already exists!'}, 400
        new_user=Users(email_id=email,password=password,name=data.get('name').strip(),role=role,status='pending' if role == 'manager' else 'active')
        db.session.add(new_user)
        db.session.commit()

        return {'message':"User signup successfully"},201