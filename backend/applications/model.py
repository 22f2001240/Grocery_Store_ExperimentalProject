from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 

db=SQLAlchemy()

#Entity 1 - User table
class Users(db.Model):
    __tablename__="users"
    id=db.Column(db.Integer,primary_key=True)
    email_id=db.Column(db.String,unique=True,nullable=False,default="example@gmail.com")
    password=db.Column(db.String(10),nullable=False)
    name=db.Column(db.String,nullable=False)
    role=db.Column(db.String,default='customer') #customer, admin, manager 
    status=db.Column(db.String,default='active') #pending,active
    cart_id=db.relationship("Cart",cascade="all,delete-orphan",backref="users",lazy=True)
    category_request_ids=db.relationship("Category_request",backref="users",lazy=True)
    orders_ids=db.relationship("Orders",cascade="all,delete-orphan",backref="users",lazy=True)
    #last_seen=db.Column(db.String(),default=datetime.now(),nullable=False) #For whther the user visited the site or not

#Entity 2 - Category table
class Category(db.Model):
    __tablename__="category"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,nullable=False)
    product_ids=db.relationship("Product",cascade="all,delete-orphan",backref="category",lazy=True)

    def convert_to_json(self):
        return{
            "id":self.id,
            "name":self.name
        }

#Entity 3 - Product table
class Product(db.Model):
    __tablename__="product"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,nullable=False)
    description=db.Column(db.String(),nullable=False)
    price=db.Column(db.Integer,nullable=False)
    unit=db.Column(db.String,nullable=False) #kg,g,m
    stock=db.Column(db.Integer,nullable=False)
    sold=db.Column(db.Integer,nullable=False) #num of sold items
    category_id=db.Column(db.Integer,db.ForeignKey("category.id"),nullable=False)
    manager_id=db.Column(db.Integer,db.ForeignKey("users.id"),nullable=False)
    #
    cart_ids=db.relationship("Cart",cascade="all,delete-orphan",backref="product",lazy=True)  #If it is not there then while delete parent it will show integrity error as foereign keys are marked as nullable =False
    orders_ids=db.relationship("Orders",cascade="all,delete-orphan",backref="product",lazy=True)
    
    def convert_to_json(self):
        return{
            "id":self.id,
            "name":self.name,
            "description":self.description,
            "price":self.price,
            "unit":self.unit,
            "stock":self.stock,
            "number_of_sold_items":self.sold,
            "category_id":self.category_id
        }

#Entity 4 - Cart table
class Cart(db.Model):
    __tablename__="cart"
    id=db.Column(db.Integer,primary_key=True)
    product_id=db.Column(db.Integer,db.ForeignKey("product.id"),nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey("users.id"),nullable=False)
    quantity=db.Column(db.Integer,nullable=False)

    def convert_to_json(self):
        return{
            "id":self.id,
            "quantity":self.quantity,
            "product_id":self.product_id,
            "product_name":self.product.name,
            "product_price":self.product.price,
            "product_unit":self.product.unit,
        }

class Orders(db.Model):
    __tablename__="orders"
    id=db.Column(db.Integer,primary_key=True)
    product_id=db.Column(db.Integer,db.ForeignKey("product.id"),nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey("users.id"),nullable=False)
    quantity=db.Column(db.Integer,nullable=False)
    date_of_purchase=db.Column(db.String,default=datetime.now(),nullable=False)

    def convert_to_json(self):
        return{
            "id":self.id,
            "quantity":self.quantity,
            "product_id":self.product_id,
            "product_name":self.product.name,
            "product_price":self.product.price,
            "product_unit":self.product.unit,
            "date_of_purchase":self.date_of_purchase,
        }

#Entity 6 - CategoryRequest table
class Category_request(db.Model):
    __tablename__="category_request"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,nullable=True)
    category_id=db.Column(db.Integer,nullable=True)
    action=db.Column(db.String,nullable=False) #CRUD
    manager_id=db.Column(db.Integer,db.ForeignKey("users.id"),nullable=False)
    def convert_to_json(self):
        return{
            "id":self.id,
            "name":self.name,
            "category_id":self.category_id,
            "action":self.action,
            "manager_id":self.manager_id
        }