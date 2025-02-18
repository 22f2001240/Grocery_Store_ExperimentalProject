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
            if get_jwt_identity().get('role') not in allowed_roles:
                return {"message":get_jwt_identity().get('role')},403
            return fn(*args,**kwargs)
        return wrapper
    return decorator
    
class CategoryRequestAPI(Resource):
    @jwt_required()  
    @roles_required(['admin','manager'])
    @cache.cached(timeout=120)
    def get(self):  
        current_user_id=get_jwt_identity().get('user_id')  
        request_json=[]
        if get_jwt_identity().get('role') == 'manager':
            requests=Category_request.query.filter_by(manager_id=current_user_id).all()
        elif get_jwt_identity().get('role') == 'admin':
            requests=Category_request.query.all()
        for req in requests:
            request_json.append(req.convert_to_json()) 
        return request_json, 200
      
    @jwt_required()    
    @roles_required(['manager'])
    def post(self):
        current_user_id=get_jwt_identity().get('user_id')
        data=request.json
        Action=data.get('action')
        if Action not in ['CREATE','UPDATE','DELETE'] or not Action:
            return {"message":"Valid action field is required"},400
        if Action=='CREATE':
            new_request=Category_request(name=data.get('name'),manager_id=current_user_id,action=Action,status='PENDING')
            db.session.add(new_request)
            db.session.commit()
            cache.clear()
            return {"message":"Request for create a new category is successful"},200
        elif Action =='UPDATE':
            cat_id= data.get('category_id')
            category=Category.query.get(cat_id)
            if not category:
                return {"message":"Category does not exist"},404
            new_request=Category_request(name=data.get('name').strip(),manager_id=current_user_id,action=Action,category_id=cat_id,status='PENDING')
            db.session.add(new_request)
            db.session.commit()
            cache.clear()
            return {"message":"Request for update the category is successful"},200
        else:
            cat_id= data.get('category_id')
            category=Category.query.get(cat_id)
            if not category:
                return {"message":"Category does not exist"},404
            new_request=Category_request(name=category.name,manager_id=current_user_id,action=Action,category_id=cat_id,status='PENDING')
            db.session.add(new_request)
            db.session.commit()
            cache.clear()
            return {"message":"Request for delete the category is successful"},200
        

class CategoryApproveAPI(Resource):
    @jwt_required()  
    @roles_required(['admin'])
    def post(self):
        data=request.json
        Action=data.get('action').strip()
        req_id=data.get('request_id')
        if Action not in ['APPROVE','REJECT'] or not Action or not req_id: # add ,'PENDING' id required.
            return {"message":"Valid action field and request id is required"},400
        cat_req=Category_request.query.get(req_id)
        if Action =="APPROVE":
            cat_req.status="APPROVED"
            db.session.commit()
            if cat_req.action =='CREATE':
                new_category=Category(name=cat_req.name)
                db.session.add(new_category)
                
                db.session.commit()
                cat_req.id = new_category.id
                db.session.commit()
                cache.clear()
                return {"message":"New category created successfuly"},200
            elif cat_req.action =='UPDATE':
                categ=Category.query.get(cat_req.category_id)
                if categ:
                    categ.name=cat_req.name
                    db.session.commit()
                    cache.clear()
                    return {"message":"Category updated successfuly"},200
                return {"message":"Category does not exist"},404
            else:
                categ=Category.query.get(cat_req.category_id)
                if categ:
                    db.session.delete(categ)
                    db.session.commit()
                    cache.clear()
                    return {"message":"Category deleted successfuly"},200
                return {"message":"Category does not exist"},404
        else:
            cat_req.status="REJECTED"
            db.session.commit()
            cache.clear()
            return {"message":"Category request rejected !!"},201



    