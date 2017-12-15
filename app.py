import rosswriter as rwriter
import plotwriter as pwriter
import lyricwriter as lwriter
import kantwriter as kwriter
import datetime
import json
import time
from flask import Flask, request

# this is how we initialize a flask application
app = Flask(__name__)


@app.route("/ross", methods=["GET"])
def gen_ross():
    sentence = rwriter.main()
    return(sentence)


@app.route("/plot/<string:ppoint>", methods=["GET"])
def gen_plot(ppoint):
    sentence = pwriter.main(ppoint)
    return(sentence)


@app.route("/lyric/<string:iartist>", methods=["GET"])
def gen_lyrics(iartist):
    sentence = lwriter.main(iartist)
    return(sentence)


@app.route("/kant/available", methods=["GET"])
def get_titles():
    """Return list of available titles"""
    list = kwriter.get_available_works()
    return(list)


@app.route("/kant/short_sentence/<string:title>", methods=["GET"])
def gen_kant_short_sentence(title):
    title = title.lower()
    if title.lower in kwriter.get_available_works():
        sentence = kwriter.get_short_sentence(title)
        return(sentence)
    else:
        return('Please submit only titles from /kant/available'), 400

@app.route("/kant/sentence/<string:title>", methods=["GET"])
def gen_kant_sentence(title):
    title = title.lower()
    if title.lower in kwriter.get_available_works():
        sentence = kwriter.get_sentence(title)
        return(sentence)
    else:
        return('Please submit only titles from /kant/available'), 400

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
