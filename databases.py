import mysql.connector
from mysql.connector import Error

def create_con(host, username, userpw, dbname):
    connection = None
    try:
        connection = mysql.connector.connect(
            host = hostname,
            user = username,
            passowrd = userpw,
            database = dbname
        )
        print("Connection successful")
    except Error as e:
        print(f'the error {e} occured')
    return connection

conn = create_con('#put endpoint link','admin', 'cis2368s26pw', 'cis2368s26db')
cursor = conn.cursor(dictionary=True) #creates vehicle named that can be used to send inputs to db and birng back records 
#Dictionary=True brings back records in the dictionary/list format easy to understand

sql = "select * from users"
cursor.execute(sql)
rows = cursor.fetchall() #Brings them back unreferenced GC finna come eat it so add reference ot the stack

for user in rows:
    print(user)
    print("The user's first name is" + user["firstname"])



