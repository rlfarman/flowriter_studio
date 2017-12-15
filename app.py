import rosswriter as rwriter
import plotwriter as pwriter
import lyricwriter as lwriter
import kantwriter as kwriter

from flask import Flask, request

# this is how we initialize a flask application
app = Flask(__name__)


@app.route("/ross", methods=["GET"])
def gen_ross():
    """Takes no input. Returns a Simulated Bob Ross statement using a markov chain."""
    sentence = rwriter.main()
    return(sentence)


@app.route("/plot/<string:plot_point>", methods=["GET"])
def gen_plot(plot_point):
    """Takes a plot point as an arguement: inciting-event, first-plot-point, first-pinch-point, midpoint, 
        second-pinch-point, third-plot-point, climax, climactic-moment, resolution, or notes. Returns a generated plot point."""
    sentence = pwriter.main(plot_point)
    return(sentence)

@app.route("/lyric/<string:artist>", methods=["GET"])
def gen_lyrics(artist):
    """Takes an artist name as an input. Returns three lines of generated lyrics based on the artist."""
    sentence = lwriter.main(artist)
    return(sentence)

@app.route("/kant/available", methods=["GET"])
def get_titles():
    """Return list of available titles"""
    list = kwriter.get_available_works()
    return(list)


@app.route("/kant/short_sentence/<string:title>", methods=["GET"])
def gen_kant_short_sentence(title):
    if title in kwriter.get_available_works():
        sentence = kwriter.get_short_sentence(title)
        return(sentence)
    else:
        return('Please submit only titles from /kant/available'), 400

@app.route("/kant/sentence/<string:title>", methods=["GET"])
def gen_kant_sentence(title):
    if title in kwriter.get_available_works():
        sentence = kwriter.get_sentence(title)
        return(sentence)
    else:
        return('Please submit only titles from /kant/available'), 400


@app.errorhandler(404)
def not_found(error):
    """Handles 404 errors"""
    return('error 404: Not found'), 404

 
if __name__ == "__main__":
    """this is run when the script is started from the command line."""

    #this is how we run the flask server, once the script is run
    app.run(host='0.0.0.0', threaded=True)
