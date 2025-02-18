from flask import Flask,request,current_app as app,flash,jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity,get_jwt #using JWT for the security
from .model import *
from .task import data_export
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
    
class ProductAPI(Resource):
    @jwt_required()  
    @cache.cached(timeout=120)
    def get(self): 
        if get_jwt_identity().get('role') in ['admin','customer']:       
            products=Product.query.all()
        if get_jwt_identity().get('role') == 'manager':
            products=Product.query.filter_by(manager_id=get_jwt_identity().get('user_id'))
        products_json=[]
        for prod in products:
            products_json.append(prod.convert_to_json()) 
        return products_json, 200
      
    @jwt_required()    #Only admin can create the category. To do this authorization is required instead of autherization. We have to check if the authenticated user has the permission to access this content / page.
    @roles_required(['manager'])
    def post(self):
        current_user_id=get_jwt_identity().get('user_id')
        print(current_user_id)
        data=request.json
        required_fields = ['name','description','price','unit','stock','category_id']
        if not all(field in data for field in required_fields):
            return {'message': 'Bad request! All fields are required.'}, 400
        name,description,price,unit,stock,sold,category_id = data.get('name'),data.get('description'),data.get('price'),data.get('unit'),data.get('stock'),0,data.get('category_id')
        if len(name) > 100 or len(name) < 3:
            return {'message': 'Product name must be at most 100 characters and atleast 3 characters long!'}, 400
        if price < 1:
            return {'message': 'Invalid Price!!'}, 400
        if stock < 0:
            return {'message': 'Invalid Stock Value!!'}, 400
        
        category = Category.query.get(category_id)
        if not category:
            return {'message':"Invalid Category !!"},404
        new_product=Product(name=name,description=description,price=price,unit=unit,stock=stock,sold=sold,category_id=category_id,manager_id=current_user_id)
        db.session.add(new_product)
        db.session.commit()
        return {'message':"Product Added successfully"},201
    
    @jwt_required()  
    @roles_required(['manager'])  
    def put(self,product_id):    
        current_user_id=get_jwt_identity().get('user_id')
        product=Product.query.get(product_id)
        if not product:
            return {'message': 'Product does not exists!'}, 404
        if product.manager_id != current_user_id: #A product can be edited by the manager who created the product
            return {'message': 'Permission denied'}, 401
        
        data=request.json
        product.name = data.get('name').strip() if data.get('name').strip() else product.name
        product.description = data.get('description') if data.get('description') else product.description
        product.price = data.get('price') if data.get('price') else product.price
        product.unit = data.get('unit') if data.get('unit') else product.unit
        product.stock = data.get('stock') if data.get('stock') else product.stock
        product.sold = data.get('sold') if data.get('sold') else product.sold
        db.session.commit()
        return {'message':"Product updated successfully"},200
    
    @jwt_required()   
    @roles_required(['manager']) 
    def delete(self,product_id): 
        current_user_id=get_jwt_identity().get('user_id')
        product = Product.query.get(product_id)
        if not product:
            return {'message': 'Product does not exists!'}, 404
        if product.manager_id != current_user_id: 
            return {'message': 'Permission denied'}, 401
        db.session.delete(product)
        db.session.commit()
        return {'message':"Product deleted successfully"},200

class ProductManagerAPI(Resource):
    @jwt_required()
    @roles_required(['manager'])
    def get(self):
        manager_id= get_jwt_identity().get('user_id')
        products = Product.query.filter_by(manager_id=manager_id).all()
        products_json=[]
        for prod in products:
            products_json.append(prod.convert_to_json())
        return products_json, 200
    

# To call the export data of products for each manager from task
class ExportDataAPI(Resource):
    @jwt_required()
    def get(self): 
        if get_jwt_identity().get('role') != 'manager':
            return {'message':'Access Denied'}, 401
        products=Product.query.filter_by(manager_id=get_jwt_identity().get('user_id')).all()
        manager=Users.query.get(get_jwt_identity().get('user_id'))
        if manager:
            product_details=[]
            for product in products:
                product_details.append({'name':product.name,'description':product.description,'price':product.price,'unit':product.unit,'stock':product.stock,'sold':product.sold})
            data_export(product_details,manager.email_id)
        return {"message":"Your data export task has been initiated, Please check your inbox"},200