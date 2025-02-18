from flask import Flask,request,current_app as app,flash,jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity,get_jwt #using JWT for the security
from .model import *
import re
from functools import wraps
from .api import *

def roles_required(allowed_roles): 
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args,**kwargs):
            if get_jwt_identity().get('role') not in allowed_roles:
                return {"message":get_jwt_identity().get('role')},403
            return fn(*args,**kwargs)
        return wrapper
    return decorator
    
class CategoryAPI(Resource):
    @jwt_required()  
    @cache.cached(timeout=120)
    def get(self):        
        categories=Category.query.all()
        category_json=[]
        for cat in categories:
            category_json.append(cat.convert_to_json()) 
        return category_json, 200
      
    @jwt_required()    #Only admin can create the category. To do this authorization is required instead of autherization. We have to check if the authenticated user has the permission to access this content / page.
    @roles_required(['admin'])
    def post(self):
        data=request.json
        required_fields = ['name']
        if not all(field in data and data[field].strip() for field in required_fields):
            return {'message': 'Bad request! All fields are required.'}, 400

        name = data.get('name')
        if len(name) > 100 or len(name) < 3:
            return {'message': 'Category name must be at most 100 characters and atleast 3 characters long!'}, 400
        
        category = Category.query.filter_by(name=name).first()
        if category:
            return {'message': 'Category already exists!'}, 400
        new_cate=Category(name=name)
        db.session.add(new_cate)
        db.session.commit()

        return {'message':"Category created successfully"},201
    
    @jwt_required()  
    @roles_required(['admin'])  
    def put(self,category_id):        
        data=request.json
        required_fields = ['name']
        if not all(field in data and data[field].strip() for field in required_fields):
            return {'message': 'Bad request! All fields are required.'}, 400

        name = data.get('name')
        if len(name) > 100 or len(name) < 3:
            return {'message': 'Category name must be at most 100 characters and atleast 3 characters long!'}, 400
        
        category = Category.query.get(category_id)
        if not category:
            return {'message': 'Category does not exists!'}, 404
        category.name=name
        db.session.commit()
        cache.clear()
        return {'message':"Category updated successfully"},200
    
    @jwt_required()   
    @roles_required(['admin']) 
    def delete(self,category_id): 
        category = Category.query.get(category_id)
        if not category:
            return {'message': 'Category does not exists!'}, 404
        db.session.delete(category)
        db.session.commit()
        # Clear cache after deletion
        cache.clear()
        return {'message':"Category deleted successfully"},200
    
class CategoryEditAPI(Resource):
    @jwt_required()
    @roles_required(['admin'])
    def get(self,category_id):
        category = Category.query.get(category_id)
        if not category:
            return {'message': 'Category does not exists!'}, 404
        return category.convert_to_json(), 200