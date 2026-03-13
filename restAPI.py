import flask
import creds
from sql import create_connection
from sql import execute_read_query
from flask import jsonify
from flask import request

app = flask.Flask(__name__)
app.config["DEBUG"] = True #allow browser to test api

@app.route('/person', methods=['POST']) #Provide raw body with json in postman
def add_person():
    request_data = request.get_json()
    firstname = request_data['firstname']
    lastname = request_data['lastname']
    
    myCreds = creds.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
    cursor = conn.cursor()

    query = "INSERT INTO person (firstname, lastname) VALUES (%s, %s)" #used ai: placeholder values are safer than concatenation
    cursor.execute(query, (firstname, lastname))
    conn.commit() #confirm changes

    return "SUCCESS"

@app.route('/job', methods=['POST']) #Provide raw body with json in postman
def add_job():
    request_data = request.get_json()
    description = request_data['description']
    startdate = request_data['startdate']
    enddate = request_data['enddate']
    
    myCreds = creds.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
    cursor = conn.cursor()

    query = "INSERT INTO job (description, startdate, enddate) VALUES (%s, %s, %s)" #used ai: placeholder values are safer than concatenation
    cursor.execute(query, (description, startdate, enddate))
    conn.commit()#confirm changes

    return "SUCCESS"

@app.route('/assignment', methods=['POST'])
def add_assignment():
    request_data = request.get_json()
    person_id = request_data['person_id']
    job_id = request_data['job_id']
    completed = request_data.get('completed', False)
    
    myCreds = creds.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
    cursor = conn.cursor()

    #prevent the person from having more than one job
    cursor.execute("SELECT 1 FROM assignment WHERE person_id = %s LIMIT 1", (person_id,)) #used ai: person cannot work more than one job at a time
    if cursor.fetchone():  #person already has a job
        return "ERROR"

    # add new assignment
    cursor.execute(
        "INSERT INTO assignment (person_id, job_id, completed) VALUES (%s, %s, %s)",
        (person_id, job_id, completed)
    )
    conn.commit()

    return "SUCCESS"

@app.route('/jobs', methods=['GET'])
def all_jobs():
    myCreds = creds.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)

    query = """
    SELECT 
        assignment.person_id,
        person.firstname,
        person.lastname,
        assignment.job_id,
        job.description
    FROM assignment
    JOIN job ON assignment.job_id = job.id
    JOIN person ON assignment.person_id = person.id;
    """

    results = execute_read_query(conn, query)

    return jsonify(results)

@app.route('/job', methods=['DELETE'])
def delete_job():
    request_data = request.get_json()
    idToBeDeleted = request_data['id']
    
    myCreds = creds.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("DELETE FROM job WHERE id = %s;", (idToBeDeleted,))#remove from table
    conn.commit()
    
    return 'SUCCESS'

app.run()