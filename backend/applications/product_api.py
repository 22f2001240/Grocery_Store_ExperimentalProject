from flask import Flask,request,current_app as app,flash,jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity,get_jwt #using JWT for the security
from .model import *
import re
from functools import wraps

# id=db.Column(db.Integer,primary_key=True)
#     name=db.Column(db.String,nullable=False)
#     description=db.Column(db.String(),nullable=False)
#     price=db.Column(db.Integer,nullable=False)
#     unit=db.Column(db.String,nullable=False) #kg,g,m
#     stock=db.Column(db.Integer,nullable=False)
#     sold=db.Column(db.Integer,nullable=False) #num of sold items
#     category_id=db.Column(db.Integer,db.ForeignKey("category.id"),nullable=False)
#     manager_id=db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)

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
    
class ProductAPI(Resource):
    @jwt_required()  
    def get(self):        
        products=Product.query.all()
        products_json=[]
        for prod in products:
            products_json.append(prod.convert_to_json()) 
        return products_json, 200
      
    @jwt_required()    #Only admin can create the category. To do this authorization is required instead of autherization. We have to check if the authenticated user has the permission to access this content / page.
    @roles_required(['manager'])
    def post(self):
        current_user_id=get_jwt_identity()
        print(current_user_id)
        data=request.json
        required_fields = ['name','description','price','unit','stock','sold','category_id']
        if not all(field in data for field in required_fields):
            return {'message': 'Bad request! All fields are required.'}, 400
        name,description,price,unit,stock,sold,category_id = data.get('name'),data.get('description'),data.get('price'),data.get('unit'),data.get('stock'),data.get('sold'),data.get('category_id')
        if len(name) > 100 or len(name) < 3:
            return {'message': 'Product name must be at most 100 characters and atleast 3 characters long!'}, 400
        if price < 1:
            return {'message': 'Invalid Price!!'}, 400
        if stock < 0:
            return {'message': 'Invalid Stock Value!!'}, 400
        if sold < 0:
            return {'message': 'Invalid Value!!'}, 400
        
        category = Category.query.get(category_id)
        if not category:
            return {'message':'Category not found'},404
        new_product=Product(name=name,description=description,price=price,unit=unit,stock=stock,sold=sold,category_id=category_id,manager_id=current_user_id)
        db.session.add(new_product)
        db.session.commit()
        return {'message':"Product Added successfully"},201
    
    @jwt_required()  
    @roles_required(['manager'])  
    def put(self,product_id):    
        current_user_id=get_jwt_identity() 
        product=Product.query.get(product_id)
        if not product:
            return {'message': 'Product does not exists!'}, 404
        if product.manager_id != current_user_id: #A product can be edited by the manager who created the product
            return {'message': 'Permission denied'}, 401
        
        data=request.json
        product.name = data.get('name').strip() if data.get('name').strip() else product.name
        product.description = data.get('description').strip() if data.get('description').strip() else product.description
        product.price = data.get('price').strip() if data.get('price').strip() else product.price
        product.unit = data.get('unit').strip() if data.get('unit').strip() else product.unit
        product.stock = data.get('stock').strip() if data.get('stock').strip() else product.stock
        product.sold = data.get('sold').strip() if data.get('sold').strip() else product.sold
        db.session.commit()
        return {'message':"Product updated successfully"},200
    
    @jwt_required()   
    @roles_required(['manager']) 
    def delete(self,product_id): 
        current_user_id=get_jwt_identity() 
        product = Product.query.get(product_id)
        if not product:
            return {'message': 'Product does not exists!'}, 404
        if product.manager_id != current_user_id: 
            return {'message': 'Permission denied'}, 401
        db.session.delete(product)
        db.session.commit()
        return {'message':"Product deleted successfully"},200