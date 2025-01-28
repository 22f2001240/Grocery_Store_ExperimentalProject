from flask import Flask,request

#create an app instance (variable to assign app)
app=Flask(__name__)

#route based api
@app.route('/api/',methods=['GET','POST'])
def home():
    return {'message':"This is a route-based api"},200

class Home(): #run by localhost/api/
    def get(self):
        return {'message':"This is a class-based get api"},200
    def post(self):
        return {'message':"This is a class-based post api"},200
    
house_api=Home()
    
@app.route('/api/class',methods=['GET','POST'])
def HomeClass():
    if request.method=='POST':
        return house_api.post()
    return house_api.get()

    

if __name__=='__main__':
    app.run(debug=True)



#thunder client is used to test api (api testing tool)
#cannot have a method in a single class twice or more
#In class based api we cannot use custom function naame . should write the function name as methods
#flask, flask_restful redis,celery,flask_cors,flask_caching,flask_jwt_extended,flask_sqlalchemy