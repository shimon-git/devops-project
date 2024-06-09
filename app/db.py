import mysql.connector
import textwrap
import atexit
from time import sleep

class DB:
    def __init__(self, host, port, db, user, password):
        self.connection_retries = 5 #Number of connection retry to the db
        
        #Tables name
        self.access_logs_table = "access_logs"
        self.counter_table = "counter"

        self.conn = self.connect_to_db(host, port, db, user, password) #Create a connection to the DB
        self.cursor = self.conn.cursor()#Create a cursor object to communicate with the DB
        self.queries = self.get_queries()##Queries for sql operations
        self.create_table() #Create the required tables of it not exist
        atexit.register(self.close) #Ensure connection is closed on exit
    
    #Connecting to db
    def connect_to_db(self, host, port, db, user, password):
        while self.connection_retries > 0:
            try:
                conn = mysql.connector.connect(#Create a connection to the DB
                    host=host,
                    port=port,
                    database=db,
                    user=user,
                    password=password
                )
                return conn #Return the connection if successful
            
            except mysql.connector.Error as e:
                print(f"Error: {e}") #Print the error message
                self.connection_retries -= 1 #Decrease the retry count
                if self.connection_retries > 0:
                    sleep(2) #Backoff for 2 secondes before retrying again
                else:
                    raise mysql.connector.Error(e) #Raise the original error if the all retries fail
                
    #Return the all needed queries for the app
    def get_queries(self):
        return {
            "create_table": {#Create table queries
                "access_log": textwrap.dedent(f'''
                    CREATE TABLE IF NOT EXISTS {self.access_logs_table} (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        client_ip VARCHAR(45),
                        internal_ip VARCHAR(45),
                        timestamp DATETIME
                    )
                '''),
                "counter": textwrap.dedent(f'''
                    CREATE TABLE IF NOT EXISTS {self.counter_table} (
                        id INT PRIMARY KEY,
                        count INT
                    )
                '''),
            },
            "insert": {#Insert queries
                "log": f'''
                    INSERT INTO {self.access_logs_table} (client_ip, internal_ip, timestamp) VALUES (%s, %s, %s)
                ''',
                "counter": f'''
                    INSERT INTO {self.counter_table} (id, count)
                    VALUES (1, %s)
                    ON DUPLICATE KEY UPDATE count = %s
                ''',
            },
            "select": {#Select queries
                "counter": f'''
                    SELECT count FROM {self.counter_table} WHERE id = 1
                '''
            }
        }
    
    #Create new table
    def create_table(self):
        #Iterate through crete table queries to create the all required tables
        for table in self.queries["create_table"]:
            self.cursor.execute(self.queries["create_table"][table])
        self.conn.commit()#Commit the changes

    #Insert new log into the access_logs table
    def insert_log(self, client_ip, internal_ip, timestamp):
        self.cursor.execute(
            self.queries["insert"]["log"],
            (client_ip, internal_ip, timestamp)
        )
        self.conn.commit()#Commit the changes

    #Get the count state from the counter
    def get_counter(self):
        self.cursor.execute(self.queries["select"]["counter"])#Run the query
        result = self.cursor.fetchone()#Fetch the first row from the cursor
        return result[0] if result is not None else 0#Return the result

    
    #Increase the counter
    def increase_counter(self):
        current_count = self.get_counter()#Get the current counter state
        new_count = current_count + 1 #Increase the counter by 1
        #Run the Insert query
        self.cursor.execute(
            self.queries["insert"]["counter"],
            (new_count, new_count)
        )
        self.conn.commit()#Commit the changes

    #Close the connection
    def close(self):
        self.cursor.close()
        self.conn.close()