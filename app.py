import rosswriter as rwriter
import plotwriter as pwriter
import lyricwriter as lwriter
 
from flask import Flask, request
 
# this is how we initialize a flask application
app = Flask(__name__)
 
@app.route("/rwriter", methods=["GET"])
def gen_ross():
    sentence = rwriter.main()
    return(sentence)

@app.route("/pwriter/<string:ppoint>", methods=["GET"])
def gen_plot(ppoint):
    sentence = pwriter.main(ppoint)
    return(sentence)

@app.route("/lwriter/<string:iartist>", methods=["GET"])
def gen_lyrics(iartist):
    sentence = lwriter.main(iartist)
    return(sentence)
 
if __name__ == "__main__":
    """
    this is run when the script is started.
    """
 
    # this is how we run the flask server, once the script is run
    app.run(host='0.0.0.0', threaded=True)
