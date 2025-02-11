from flask import Flask,request,current_app as app,flash,jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity,get_jwt 
from .model import *
import re
from functools import wraps
from .api import *

def roles_required(allowed_roles): 
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args,**kwargs):
            if get_jwt().get("role") not in allowed_roles:
                return {"message":"Access denied!"},403
            return fn(*args,**kwargs)
        return wrapper
    return decorator
    
class CartAPI(Resource):
    @jwt_required()  
    @roles_required(['customer'])
    @cache.cached(timeout=120)
    def get(self):  
        current_user_id=get_jwt_identity()     
        carts=Cart.query.all()
        carts_json=[]
        cart_total=0
        for item in carts:
            carts_json.append(item.convert_to_json()) 
            cart_total+= item.quantity * item.product.price
        return {"Cart Products":carts_json,"Total cart value":cart_total}, 200
      
    @jwt_required()    
    @roles_required(['customer'])
    def post(self):
        current_user_id=get_jwt_identity()
        data=request.json
        required_fields = ['quantity','product_id']
        if not all(field in data for field in required_fields):
            return {'message': 'Bad request! All fields are required.'}, 400
        quantity=data.get('quantity')
        product_id=data.get('product_id')
        if quantity < 1:
            return {'message': 'Invalid Value!!'}, 400
        product = Product.query.get(product_id)
        if not product:
            return {'message':'Product not found'},404
        cart=Cart.query.filter_by(user_id=current_user_id,product_id=data.get('product_id')).first()
        if cart:
            cart.quantity=quantity
            db.session.commit()
            return {'message':"Quantity updated successfully"},200
        new_item=Cart(quantity=quantity,product_id=product_id,user_id=current_user_id)
        db.session.add(new_item)
        db.session.commit()
        return {'message':"Item Added successfully into the cart"},201
    
    @jwt_required()  
    @roles_required(['customer'])  
    def patch(self,cart_id):    
        current_user_id=get_jwt_identity() 
        cart=Cart.query.filter_by(id=cart_id,user_id=current_user_id).first()
        if not cart:
            return {'message':'Cart not found'},404
        data=request.json
        required_fields = ['quantity']
        if not all(field in data for field in required_fields):
            return {'message': 'Bad request! All fields are required.'}, 400
        quantity=data.get('quantity')
        cart.quantity=quantity
        db.session.commit()
        return {'message':"Quantity updated successfully"},200
    
    @jwt_required()   
    @roles_required(['customer']) 
    def delete(self,cart_id): 
        current_user_id=get_jwt_identity() 
        cart=Cart.query.filter_by(id=cart_id,user_id=current_user_id).first()
        if not cart :
            return {'message':'Cart not found'},404
        if cart.user_id != current_user_id: 
            return {'message': 'Permission denied'}, 401
        db.session.delete(cart)
        db.session.commit()
        return {'message':"Product removed from cart successfully"},200