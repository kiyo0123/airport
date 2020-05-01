import json
import os
from flask import Flask
from google.cloud import spanner

app = Flask(__name__)

instance_id = 'tokyo-spanner'
database_id = 'testdb'
spanner_client = spanner.Client()
instance = spanner_client.instance(instance_id)
database = instance.database(database_id)

@app.route('/')
def hello():
    return "hey, I'm working... it's true."

@app.route('/airports/<string:code>/')
def airports(code):
    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(
            "SELECT * from Airports WHERE iata_code = '%s'" % code
        )
    l = []
    for row in results:
        print(row)
        l.append(row)
    
    if len(l) == 0:
        return json.dumps("Not Found.")
    #return str(l[0])
    return json.dumps(l[0]) # TODO: return json objects

@app.route('/airportname/<string:code>/')
def airportname(code):
    with database.snapshot() as snapshot:
        results = snapshot.execute_sql(
            "SELECT * from Airports WHERE iata_code = '%s'" % code
        )
    l = []
    for row in results:
        print(row)
        l.append(row)
    
    if len(l) == 0:
        return "Not Found."
    return l[0][2]

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
