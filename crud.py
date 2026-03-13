import mysql.connector
import creds
from mysql.connector import Error
from sql import create_connection
from sql import execute_query
from sql import execute_read_query

#create connection to mysql
myCreds = creds.Creds()
conn = create_connection(myCreds.constring, myCreds.userName, myCreds.password, myCreds.dbName)

#add new entry to our users table
query = "INSERT INTO users (firstname, lastname) VALUES ('Thomas', 'Edison')"
execute_query (conn, query)

#get all users
select_users = "SELECT * FROM users"
users = execute_read_query(conn, select_users)

for user in users:
    print (user ["firstname"]+ " has the last name: " +user["lastname"])

#add a table for invoices
create_invoice_table = """
CREATE IF NOT EXISTS invoices(
id INT AUTO_INCREMENT,
amount INT,
description VARCHAR(255) NOT NULL,
user_id INT UNSIGNED NOT NULL,
FOREIGN KEY fk_user_id(user_id) REFRENCES users (id),
PRIMARY KEY (id)
)"""

execute_query(conn, create_invoice_table)

#add invoice to invoice table
invoice_from_user = 1
invoice_amount = 50
invoice_description = "Harry Potter Books"
query = "INSERT INTO invoices (amount, description, user_id) VALUES (%s, '%s', %s)" (invoice_amount, invoice_description, invoice_from_user)
#execute_query(conn, query)


#update invoice record
new_amount = 30
update_invoice_query = """
UPDATE invoices
SET AMOUNT = %s
WHERE id = %s""" % (new_amount, invoice_from_user)
#execute_query (conn, update_invoice_query)

#delete invoice from invoice table
invoice_id_to_delete = 1
delete_statement = "DELETE FROM invoices WHERE id = %s" % (invoice_id_to_delete)
#execute_query (conn, update_invoice_query)

#delete table
delete_table_statment = "DROP TABLE invoices"
execute_query (conn, delete_table_statment)