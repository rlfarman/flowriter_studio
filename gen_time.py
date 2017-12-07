"""
script to give datetime and millisecond time conversion functionality
"""
 
import datetime
import json
import time
 
from flask import Flask, request
 
# this is how we initialize a flask application
app = Flask(__name__)
 
 
@app.route("/timestamp", methods=["GET"])
def get_timesptamp_millis():
    """
    method that return the current date and time as a millisecond integer
    :return: integer
    """
    current_time = time.time()
    time_millis = int(round(current_time * 1000))
 
    print("time in millis is:", time_millis)
 
    return(str(time_millis))
 
 
@app.route("/datetime", methods=["POST"])
def get_datetime():
    """
    method that takes in milliseconds integer and returns date time in format dd/mm/yyyy hh:mm:ss
    :return: datetime string
    """
 
    # the time in millis will be in the request body and we cn access it using the request object provided by
    # the flask module
 
    request_body = json.loads(request.data)
    millis_time = int(request_body["millis"])
    date_time_gen = datetime.datetime.fromtimestamp(millis_time / 1000)
 
    print("the date time is:", date_time_gen)
 
    return(str(date_time_gen))
 
 
if __name__ == "__main__":
    """
    this is run when the script is started.
    """
 
    # this is how we run the flask server, once the script is run
    app.run(host='0.0.0.0', threaded=True)
