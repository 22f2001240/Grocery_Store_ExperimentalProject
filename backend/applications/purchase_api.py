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
    
class OrderAPI(Resource):
    @jwt_required()  
    @roles_required(['customer'])
    @cache.cached(timeout=120)
    def get(self):  
        current_user_id=get_jwt_identity()     
        orders=Orders.query.filter_by(user_id=current_user_id).all()
        orders_json=[]
        for order in orders:
            orders_json.append(order.convert_to_json()) 
        return orders_json, 200
      
    @jwt_required()    
    @roles_required(['customer'])
    def post(self):
        current_user_id=get_jwt_identity()
        cart_items=Cart.query.filter_by(user_id=current_user_id).all()
        if len(cart_items) < 1:
            return {'message':"Your cart is empty"},400
        item_list=[]
        for item in cart_items:
            product=Product.query.get(item.product_id)
            quant=product.stock
            if item.quantity > quant:
                return {'message':"Out of stock !!"},400
            product.stock=quant-item.quantity
            product.sold=product.sold+item.quantity
            new_order=Orders(product_id=item.product_id,quantity=item.quantity,user_id=current_user_id)
            db.session.add(new_order)
            db.session.delete(item)
        db.session.commit()
        return {'message':"Order Successful.Thank you shopping!!"},201
        #     item_list.append({'id':item.id,'quantity':item.quantity})
        # return {'message':item_list},201

    