from flask import Flask, render_template
from markov import MarkovLyrics

# Create an instance of a Flask application
app = Flask(__name__) #four underscores total

# Our home route
@app.route('/')
def lyricsGenerator():
    data = ["cow dog bunny dog cow horse", "dog cat dog cat"]
    m = MarkovLyrics()
    m.populateMarkovChain(data)
    print(m.generateLyrics())    
    
    return render_template('home.html')

if __name__ == '__main__':
    app.run()