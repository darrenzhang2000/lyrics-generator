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

    song = m.generateLyrics()
    lines = song.split("NEWLINE")

    return lines

# Our home route
@app.route('/', methods = ['GET', 'POST'])
def lyricsGenerator():
    lines = []
    if request.method == 'POST':
        artist = request.form['search']
        lines = generateArtistSong(artist)
    return render_template('home.html', lines=lines)

if __name__ == '__main__':
    app.run()