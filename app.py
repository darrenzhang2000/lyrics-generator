from flask import Flask, render_template, request
from markov import MarkovLyrics
from lyrics import webScrapeLyrics


# Create an instance of a Flask application
app = Flask(__name__) #four underscores total

def generateArtistSong(name):
    songs_array = webScrapeLyrics(name)
    m = MarkovLyrics()
    # Populate the markov chain using all 10 songs
    for song in songs_array:
        # Recall that each song contains an array of lyrics
        m.populateMarkovChain(song)
    return m.generateLyrics()

# Our home route
@app.route('/', methods = ['GET', 'POST'])
def lyricsGenerator():
    song = ""
    if request.method == 'POST':
        artist = request.form['search']
        song = generateArtistSong(artist)
    return render_template('home.html', song=song)



if __name__ == '__main__':
    app.run()