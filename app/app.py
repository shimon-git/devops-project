from flask import Flask, request, make_response
import socket
from datetime import datetime
from db import DB


class App:
    def __init__(self, app_conf):
        self.app = Flask(__name__) #Initialize a new flask instance
        self.setup_routes()#Setup the routes
        self.db = DB(#Initialize a new DB instance
            host=app_conf["host"],
            port=app_conf["port"],
            db=app_conf["database"],
            user=app_conf["user"],
            password=app_conf["password"]
        )


    def setup_routes(self):
        #Handler for "/" route
        @self.app.route("/")
        def index():
            client_ip = request.remote_addr #Retrieve the client IP
            internal_ip = socket.gethostbyname(socket.gethostname()) #Retrieve the internal IP
            time_stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")#Create a formatted time stamp to log the request

            self.db.insert_log(client_ip,internal_ip,time_stamp) #Save access log
            self.db.increase_counter() #Increase the global counter

            response = make_response(f"Internal IP: {internal_ip}") #Create the response
            response.set_cookie("internal_ip",internal_ip, max_age=60*5) #Create a cookie with the internal IP
            
            return response #Return the response to the client
        
        #Handler for "/showcount" route
        @self.app.route("/showcount")
        def show_count():
            return f"Global Counter: {self.db.get_counter()}" #Return The global counter number
    
    #Start the flask app
    def run(self, host="0.0.0.0", port=5000):
        self.app.run(host=host, port=port)
