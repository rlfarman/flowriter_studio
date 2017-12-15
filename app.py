import rosswriter as rwriter
import plotwriter as pwriter
import lyricwriter as lwriter
import promptwriter as prwriter

from flask import Flask, request

# this is how we initialize a flask application
app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    """Creates the homepage"""
    return('''<div>
                    <h1>Welcome to Flowriter</h1>
              </div>
              <div>
                    <h3>The api endpoints are at:</h3>
                    <ol><a href="/ross">/ross</a></ol>
                    <ol><a href="/plot/climax">/plot/plot_point</a></ol>
                    <ol><a href="/lyric/drake>"/lyric/artist</a></ol>
                    <ol><a href="/prompt">/prompt</a></ol>
              </div>'''
            )

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

@app.route("/prompt", methods=["GET"])
def gen_prompt():
    """Takes no input. Returns a generated writing prompt."""
    sentence = prwriter.main()
    return(sentence)

@app.errorhandler(404)
def not_found(error):
    """Handles 404 errors"""
    return('error 404: Not found')

 
if __name__ == "__main__":
    """this is run when the script is started from the command line."""

    #this is how we run the flask server, once the script is run
    app.run(host='0.0.0.0', threaded=True)
