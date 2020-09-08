from flask import Flask, render_template
from markov import MarkovLyrics
from lyrics import webScrapeLyrics

# Create an instance of a Flask application
app = Flask(__name__) #four underscores total

# Our home route
@app.route('/')
def lyricsGenerator():
    songs_array = webScrapeLyrics("Kendric Lamar")
    m = MarkovLyrics()
    # Populate the markov chain using all 10 songs
    for song in songs_array:
        # Recall that each song contains an array of lyrics
        m.populateMarkovChain(song)
    print(m.generateLyrics())    

    return render_template('home.html')

if __name__ == '__main__':
    app.run()