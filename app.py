import rosswriter as rwriter
import plotwriter as pwriter
import lyricwriter as lwriter

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


 
if __name__ == "__main__":
    """
    this is run when the script is started.
    """

    # this is how we run the flask server, once the script is run
    app.run(host='0.0.0.0', threaded=True)
