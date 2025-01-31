from flask import Flask,request,current_app as app,flash,jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity,get_jwt #using JWT for the security
from .model import *
import re
from functools import wraps

#200-okey , 201-create a new record,404-not found, 400-bad request, 401-authentication issue, 403 auth, 405-method not found
        
class WelcomeAPI(Resource):
    @jwt_required()
    def get(self):
        print(get_jwt().get("role"))
        return {'message':'Hello, This is GroceryStore!'},200
    def post(self):
        data=request.json #or can use request.get_json()
        print(request)
        print(data)
        msg=f'Hello {data.get("name")}!!'
        return {'message':msg},200
    

    #     current_user=get_jwt_identity()
    #     if current_user['role']!= 'admin': # Authentication
    #         return {'message':'Access Denied'},401