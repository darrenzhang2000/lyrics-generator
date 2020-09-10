# Generate music styled after your favorite music artist with Python and Flask 

#### In this tutorial, we will be building the Lyrics Generator using Python and Flask. 

Darren Zhang - September 9, 2020

Here is what the final product looks like:

![image](https://user-images.githubusercontent.com/44158788/92673159-748db580-f2e8-11ea-9daf-7e436ce0a576.png)


Here’s what you’ll learn:
* Use the Requests module in Python
* Make API get/post requests.
* Web scrape using Beautiful Soup
* Basic markov chains theory
* Create a Python markov chain class 
* Using markov chains to generate next possible words
* Search for music artists, generate songs, and render result in Flask

Feel free to checkout my code on GitHub at any point during this tutorial. https://github.com/darrenzhang2000/lyrics-generator

### Get a music artist’s top ten songs lyrics: 
### Part 1 (Workflow)
In this section, we will be using the genius api to get a music artist’s top 10 songs. Because we will need to make multiple API calls to get the results that we want, I’ve divided this task into two sections. Part 1 is workflow for this task and part 2 is the code for this task.

Our first step is to create an API client, which is your unique identifier that can be used to make API calls. Follow the instructions here to create your API Client: [https://docs.genius.com/#/getting-started-h1](https://docs.genius.com/#/getting-started-h1)

We will be testing our APIs with Postman. If you don’t have it already, download it here: [https://www.postman.com/downloads/](https://www.postman.com/downloads/)

We can use the search resource, as shown in the docs, to search for specific artists: [https://docs.genius.com/#search-h2](https://docs.genius.com/#search-h2)
The q is a query parameter, which are extensions of the URL that are used to help define specific content. Since we are querying for music artists, we just set q to whatever music artist we want to search. We can use the “sort” query parameter to 
Let’s test out this example in Postman: 

![image](https://user-images.githubusercontent.com/44158788/92673197-8ff8c080-f2e8-11ea-9f30-2ea6e87e57fa.png)


Note that %20 is the encoded representation of a space. The string after Bearer is the Client Access Token which we obtained from our API Client.

Here is the result returned: 

![image](https://user-images.githubusercontent.com/44158788/92673217-98e99200-f2e8-11ea-9df6-ff244dab2b63.png)


Here are the results from the docs itself:
As you can see, hits is an array which contains the top ten songs for the specified artist. Inside each “hit” object, there is a “result” object which contains details about the songs. 

![image](https://user-images.githubusercontent.com/44158788/92673232-a0a93680-f2e8-11ea-9f41-0be7b3d75774.png)

![image](https://user-images.githubusercontent.com/44158788/92673240-a6068100-f2e8-11ea-98b9-ee758f9c8191.png)


Nested inside “results” is the “primary_artist” object.

![image](https://user-images.githubusercontent.com/44158788/92673269-b9b1e780-f2e8-11ea-9605-93769c347d74.png)


Perfect! Now that we’ve identified the artist’s id, we can use that to get the top ten songs by that artist. We will use GET /artists/:id/songs :[https://docs.genius.com/#artists-h2](https://docs.genius.com/#artists-h2)


![image](https://user-images.githubusercontent.com/44158788/92673274-c0405f00-f2e8-11ea-88de-ad5055ce7256.png)

Notice that by default, the api returns 20 songs sorted by title. Let’s modify this so that we get the top 10 most popular songs.



In Postman, enter the following (also make sure that you have the authorization token in the header like in previous examples):

![image](https://user-images.githubusercontent.com/44158788/92673292-ca625d80-f2e8-11ea-89df-b4be4fafa785.png)

Notice that by entering the key value pairs in the form, Postman automatically appends these values to the url. This is the response that we get: 

![image](https://user-images.githubusercontent.com/44158788/92673297-ce8e7b00-f2e8-11ea-8dc1-a5889e2c3c3c.png)


If we click on one of the songs and navigate towards the bottom, we get the following: 

![image](https://user-images.githubusercontent.com/44158788/92673309-d4845c00-f2e8-11ea-9806-58e19208d316.png)

If we open that url into a browser, we get the actual lyrics of the song:

![image](https://user-images.githubusercontent.com/44158788/92673319-d9491000-f2e8-11ea-86dc-df9886d8af5b.png)


Great! This is exactly what we want. 


#### Let’s recap our workflow:
Search for a music artist by sending an API request to api.genius.com/artists.
Note that we need to pass in the authorization bearer as part of the headers.
q is the query parameter where we input our music artist’s name.
https://docs.genius.com/#search-h2   
Get the music artist’s ID using the response obtained from step 1.
The nesting is as follows: response -> hits[0] -> result -> primary_arist -> id
Get the top ten songs by the artist using the id obtained from step 2.
The possible query parameters are id, sort, per_page, and page.
https://docs.genius.com/#artists-h2  
For each of these songs, retrieve the url to the lyrics link and store these in an array.
The nesting is as follows: response -> songs array -> url
### Get a music artist’s top ten songs lyrics: 
### Part 2 (Code)

![image](https://user-images.githubusercontent.com/44158788/92673332-de0dc400-f2e8-11ea-9be4-171670e181b4.png)


Now that we have the workflow, let’s code this up. Create a dictionary called lyrics-generator or whatever name of your choice. Inside this directory, create 3 files, app.py, lyrics.py and config.ini. 


Config.ini is a file where you store configurations, some of which you may not want to publicly reveal. If you were to push code on Github for instance, it would be a good idea to keep sensitive configurations hidden. In that case, create a .gitignore file and config.ini in that file.

![image](https://user-images.githubusercontent.com/44158788/92673342-e2d27800-f2e8-11ea-8464-a8ec42394f44.png)



Optional: Here is an article on why you should hide your API keys: [https://www.freecodecamp.org/news/how-to-securely-store-api-keys-4ff3ea19ebda/](https://www.freecodecamp.org/news/how-to-securely-store-api-keys-4ff3ea19ebda/)

In lyrics.py, let’s write a function to get this token. Also make sure you have the configparser library installed. If not, run pip install configparser.
```
import configparser
 
def getAccessToken():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['Client_Access_Token']['token']
token = getAccessToken()
print(token)
```

#### Let’s follow step 1 of our workflow: 
Search for a music artist by sending an API request to api.genius.com/artists.

Import the requests library by running in your terminal:  pip install requests.

We create a function which accepts a name argument and passes in the name as a query parameter using Python’s format string. Then, we make a get request using the requests library and return the result:
```
def searchMusicArtist(name):
    api_url = "http://api.genius.com/search?q={}".format(name)
    print(api_url)
    r = requests.get(api_url)
    return r.json()
 
print(searchMusicArtist("Kendrick Lamar"))
```

Here is the output from the terminal:

![image](https://user-images.githubusercontent.com/44158788/92674034-7fe1e080-f2ea-11ea-9b12-eef9e2f6ea50.png)


Uh … not exactly what we want. A quick google search suggests that this is because the request has not been applied because it lacks authentication credentials. To fix this, we need to pass in our API access token as part of our headers. 

```
def searchMusicArtist(name):
    api_url = "http://api.genius.com/search?q={}".format(name)
    headers = {"authorization": token}
    print(api_url)
    r = requests.get(api_url, headers=headers)
    return r.json()
 
print(searchMusicArtist("Kendrick Lamar"))
```

![image](https://user-images.githubusercontent.com/44158788/92674045-853f2b00-f2ea-11ea-9022-e531a3cede6c.png)


Great! We got a success message.

Let’s view the results:
```
print(searchMusicArtist("Kendrick Lamar")["response"])
```

![image](https://user-images.githubusercontent.com/44158788/92674072-95efa100-f2ea-11ea-9fac-c6dd78084e09.png)


#### Onto step 2! 
Get the music artist’s ID using the response obtained from step 1.
The nesting is as follows: response -> hits[0] -> result -> primary_arist -> id

Let’s abstract this logic into a function called getArtistId.
```
def getArtistId(name):
    r = searchMusicArtist(name)
    id = r["response"]["hits"][0]["result"]["primary_artist"]["id"]
    return id
 
print(getArtistId("Kendrick Lamar"))
```

Notice that we called the searchMusicArtist function we created earlier.

Challenge: do steps 3 and 4 yourself. 

Answers:

#### Step 3: 
Get the top ten songs by the artist using the id obtained from step 2.
The possible query parameters are id, sort, per_page, and page.
GET /artists/:id/songs
[https://docs.genius.com/#artists-h2  ](https://docs.genius.com/#artists-h2)

Following in step 1’s footsteps, we get:
```
def getTopTenSongs(name):
    id = getArtistId(name)
    api_url = "http://api.genius.com/artists/{}/songs".format(id)
    headers = {"authorization": token}
    r = requests.get(api_url, headers=headers)
    return r.json()
 
print(getTopTenSongs("Kendrick Lamar")["response"])
```

Now let’s modify this so that rather than getting 20 songs sorted by title (this is the default which is specified in the API documentation), let’s add the query params to get the top 10 songs and sort by popularity:

```
def getTopTenSongs(name):
    id = getArtistId(name)
    api_url = "http://api.genius.com/artists/{}/songs".format(id)
    headers = {"authorization": token}
    params = {
        "sort": "popularity",
        "per_page": 10
    }
    r = requests.get(api_url, headers=headers, params=params)
    return r.json()
 
print(getTopTenSongs("Kendrick Lamar")["response"])
```

Passing in params is quite similar to passing in headers. Alternatively, we could have also used string formatting to pass the params to the api url. 

#### Onto the last step for this section. 
#### Step 4: 
For each of these songs, retrieve the url to the lyrics link and store these in an array.
The nesting is as follows: response -> songs array -> url

```
def getLyricsArray(name):
    r = getTopTenSongs(name)
    songs = r["response"]["songs"]
    print(songs)
 
print(getLyricsArray("Kendrick Lamar"))
```

This will give us a list containing song objects: 

![image](https://user-images.githubusercontent.com/44158788/92674096-a0aa3600-f2ea-11ea-8956-3c3e52930174.png)



Here is what a song object inside the song array looks like:

![image](https://user-images.githubusercontent.com/44158788/92674399-3ba31000-f2eb-11ea-8d65-f33b4f964915.png)

We want to store this url in an array. Let’s loop through each of the song objects and do just that. 

![image](https://user-images.githubusercontent.com/44158788/92674417-42ca1e00-f2eb-11ea-9664-20292b8c637a.png)

```
def getLyricsArray(name):
    r = getTopTenSongs(name)
    songs = r["response"]["songs"]
    lyrics_array = []
    for song in songs:
        lyrics_array.append(song["url"])
    return lyrics_array
 
print(getLyricsArray("Kendrick Lamar"))
```
![image](https://user-images.githubusercontent.com/44158788/92674435-49589580-f2eb-11ea-9078-af614b9a2b53.png)

And we’re done!!
The code up to this point can be found in branch1 of my github repo: [https://github.com/darrenzhang2000/lyrics-generator/blob/branch1/lyrics.py](https://github.com/darrenzhang2000/lyrics-generator/blob/branch1/lyrics.py)



### Web scrape song lyrics
In this section, we will use Beautiful Soup to web scrape the lyrics from each of the urls in the lyrics array. 

Begin by looping through the lyrics array and printing out the urls.
```
def webScrapeLyrics(name):
    arr = getLyricsArray("Kendrick Lamar")
    for el in arr:
        print(el)
 
webScrapeLyrics("Kendrick Lamar")
```

![image](https://user-images.githubusercontent.com/44158788/92674444-4fe70d00-f2eb-11ea-8635-94b34b265f3d.png)


If we open any of these urls and inspect the html page, we’ll see that all of the lyrics are inside a class called lyrics.

![image](https://user-images.githubusercontent.com/44158788/92674462-5a090b80-f2eb-11ea-8c9e-fec63670dd4c.png)

Let’s get hold of this class by using Beautiful Soup. If you don’t have Beautiful Soup installed, then run in your terminal: pip install beautifulsoup4

Now import it as follows: 
```
from bs4 import BeautifulSoup

def webScrapeLyrics(name):
    arr = getLyricsArray("Kendrick Lamar")
    for url in arr:
        page = requests.get(url)
        print(page)
        soup = BeautifulSoup(page.content, 'html.parser')
```

Here, page is the html response that is returned when we navigate to the url. We use the BeautifulSoup constructor to get hold and parse this html page. To get hold of specific elements, call the find method and pass in the attribute you want to search by. More info can be found here: https://www.crummy.com/software/BeautifulSoup/bs4/doc/ . We will find by passing in class_. Note that the underscore is necessary because class is a reserved keyword in Python. 

```
def webScrapeLyrics(name):
    arr = getLyricsArray("Kendrick Lamar")
    for url in arr:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        lyrics_div = soup.find(class_="lyrics")
        print(lyrics_div, '\n')
 
webScrapeLyrics("Kendrick Lamar")
```

The actual lyrics text is contained within “a” tags. For each of these “a” tags, we can access the text inside it by using .text .

![image](https://user-images.githubusercontent.com/44158788/92674470-5f665600-f2eb-11ea-9082-4e7708204ccd.png)

```
def webScrapeLyrics(name):
    arr = getLyricsArray("Kendrick Lamar")
    for url in arr:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        lyrics_div = soup.find(class_="lyrics")
        lyrics_links = lyrics_div.find_all('a')
        for link in lyrics_links:
            print(link.text, '\n')
 
webScrapeLyrics("Kendrick Lamar")
```

![image](https://user-images.githubusercontent.com/44158788/92674477-655c3700-f2eb-11ea-9cbd-67c659c43dcb.png)

Very close! However, notice that if the text encased by brackets is not part of the lyrics. We can use an if statement to exclude these.

Addition to that, let’s create an array called songs_lyrics, to contain the lyrics of these 10 songs. Each element inside songs_lyrics is an array containing the lines for each song.
```
def webScrapeLyrics(name):
    arr = getLyricsArray("Kendrick Lamar")
    songs_lyrics = []
    for url in arr:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        lyrics_div = soup.find(class_="lyrics")
        lyrics_links = lyrics_div.find_all('a')
        current_lyrics = []
        for link in lyrics_links:
            if len(link.text) > 0 and link.text[0] != "[":
                current_lyrics.append(link.text)
        songs_lyrics.append(current_lyrics)
    return songs_lyrics
print(webScrapeLyrics("Kendrick Lamar"))
```

If we run this, however, there is a small problem - newlines are encoded as ‘\n ’. Let's just replace it with a space. 

![image](https://user-images.githubusercontent.com/44158788/92674503-7ad16100-f2eb-11ea-9745-66558e177bf5.png)

```
def webScrapeLyrics(name):
    arr = getLyricsArray("Kendrick Lamar")
    songs_lyrics = []
    for url in arr:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        lyrics_div = soup.find(class_="lyrics")
        lyrics_links = lyrics_div.find_all('a')
        current_lyrics = []
        for link in lyrics_links:
            if len(link.text) > 0 and link.text[0] != "[":
                text = link.text.replace("\n", " ")
                current_lyrics.append(text)
        songs_lyrics.append(current_lyrics)
    return songs_lyrics
print(webScrapeLyrics("Kendrick Lamar"))
```

That’s it for this section. The code up to this point can be found in branch2 of my github repo: https://github.com/darrenzhang2000/lyrics-generator/blob/branch2/lyrics.py


### A Brief Introduction to Markov Chains
Markov chains are mathematical systems that hop from one "state" (a situation or set of values) to another. For example, if you made a Markov chain model of a baby's behavior, you might include "playing," "eating", "sleeping," and "crying" as states. If a baby’s current state is “playing”, the next possible states would be (continue) “playing”, “eating”, “sleeping” and “crying”. Suppose the baby decides to sleep. Then the next possible states would be to either wake up or continue sleeping. Feel free to check out this article on Markov Chains: https://setosa.io/ev/markov-chains/

For this project, we will be using Markov Chains to find the next possible words for a given word. 

### Creating the Markov Chain Class
Start by creating a file called markov.py. Create a class called MarkovLyrics with the chain initialized as an empty dictionary. Create the constructor as follows:
```
class MarkovLyrics:
    def __init__(self):
        # A dictionary containing phrases (each phrase contains self.order number of words)
        # Example 
        # self.chain = {
        #   "baby": [plays, sleeps, crawls, sleeps],
        #   "plays": [toy, food],
        #   ...
        # }
        self.chain = {}
```
The dictionary contains a list of words as keys, and their values are the possible next words. For example, there are four possible words after baby. Notice that “baby sleeps” is likelier than “baby crawls” because “baby sleeps” occur twice in the array.

Now let’s create a method for the MarkovLyrics class that populates the markov chain. We will read in a lyrics array (which we created earlier). Then, create an array with each word in the string. Loop through this words array and for each word, add next_word to the possibilities array for the current word. 
```
    def populateMarkovChain(self, lyrics):
        for line in lyrics:
            words = line.split(" ")
            # For every possible starting index of the word  
            for i in range(len(words) - 1):
                word = words[i]
 
                # If the word is already in the dictionary, 
                # append next_word to the list of possible words
                # for the word
                if word in self.chain:
                    next_word = words[i + 1]
                    self.chain[word].append(next_word)
 
                # First time this word occurs
                # next_word is the only possible next word right now
                else:
                    next_word = words[i + 1]
                    self.chain[word] = [next_word]
```
Let’s test it.
```
data = ["cow dog bunny dog cow horse", "dog cat dog cat"]
 
m = MarkovLyrics()
m.populateMarkovChain(data)
print(m.chain)
```

And the result:
![image](https://user-images.githubusercontent.com/44158788/92674493-7016cc00-f2eb-11ea-8bcf-f8eba286e871.png)


Now that we have the chain,  let’s use it to generate lyrics. Start by choosing a random word from the list of keys.
```
    # length is the length so the song we generate
    def generateLyrics(self, length=500):
        n = len(self.chain)
 
        # Choose a random starting word
        start_index = randint(0, n - 1)
        keys = list(self.chain.keys())
        cur_word = keys[start_index]
        # capitalize first character
        cur_word = cur_word[0].upper() + cur_word[1:]
 
        # result string
        res = cur_word + " "
```
Next, we want to choose the next word from the list of possible words in the chain. To choose the word after that, next_word becomes the current word. We want to repeat this a certain amount of times, specified by the variable length (I set the default value to 500). 
```
        for _ in range(length):
                possible_words = self.chain[cur_word]
                index = randint(0, len(possible_words) - 1)
                next_word = possible_words[index]
                res += next_word + ' '
                cur_word = next_word
        return res
 ```

However, consider the following sentence: “hello world”. This will build the following dictionary: {“hello”: [“world”] } . Once the current word becomes “world”, we run into a problem because “world” doesn’t have any possible next words. In that case, let’s just add a new line and choose a new starting word.
```
    # length is the length so the song we generate
    def generateLyrics(self, length=500):
        n = len(self.chain)
 
        # Choose a random starting word
        start_index = randint(0, n - 1)
        keys = list(self.chain.keys())
        cur_word = keys[start_index]
        # capitalize first character
        cur_word = cur_word[0].upper() + cur_word[1:]
 
        # result string
        res = cur_word + " "
 
        for _ in range(length):
            if cur_word not in self.chain:
                res += '\n'
                next_index = randint(0, len(self.chain) - 1)
                l = list(self.chain)
                cur_word = l[next_index]
            else:
                possible_words = self.chain[cur_word]
                index = randint(0, len(possible_words) - 1)
                next_word = possible_words[index]
                res += next_word + ' '
                cur_word = next_word
        return res
 
 

data = ["cow dog bunny dog cow horse", "dog cat dog cat"]
m = MarkovLyrics()
m.populateMarkovChain(data)
print(m.generateLyrics())
```

The final code for this file can be found on branch3 of my GitHub: https://github.com/darrenzhang2000/lyrics-generator/blob/branch3/markov.py

Note that for simplicity, our current word only depends on the previous word. If our current word were to depend on the previous two or three words, instead of just one, the program would take longer to run but the lyrics generated would be better. As a challenge, feel free to modify our code to depend on the previous n words. 



### Using the Markov Lyrics Class in Our Flask App
Now that we’re done creating this class, let’s use it in our project. Let’s begin by creating our Flask website. Create a dictionary called templates and a home.html file in that directory. 

Generate the html boilerplate in your home.html and the basic layout for our page:
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <h1>Welcome to Lyrics Generator!</h1>
    <p>Here, you can generate lyrics by the artist of your choice!</p>
    <form>
        <input type="text" id="search" name="search" placeholder="Search for an artist...">
        <input type="submit">
    </form>
</body>
</html>
 ```

Create a file called app.py. Inside this file, we will render home.html as the default route ‘/’. Make sure you import flask: pip install Flask

```
from flask import Flask, render_template
 
# Create an instance of a Flask application
app = Flask(__name__) #four underscores total
 
# Our home route
@app.route('/')
def lyricsGenerator():
    return render_template('home.html')
 
if __name__ == '__main__':
    app.run()
```

Run python app.py in your terminal and click on the url. 

![image](https://user-images.githubusercontent.com/44158788/92674514-80c74200-f2eb-11ea-8e59-cfb13fa1fb19.png)

![image](https://user-images.githubusercontent.com/44158788/92674528-8886e680-f2eb-11ea-9811-39b64c1e1ed7.png)


Import the MarkovLyrics class and test it using our dummy data to make sure everything is working:

```
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
```

Run the app, click on the url and you should get the following:

![image](https://user-images.githubusercontent.com/44158788/92676445-8d4d9980-f2ef-11ea-8be4-b9adfacbba21.png)


Now, let’s import the webScrapeLyrics function in lyrics.py. (Also be sure to delete any print statements we used for testing earlier). 
```
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
```
![image](https://user-images.githubusercontent.com/44158788/92676509-afdfb280-f2ef-11ea-80a4-86dda14b4bc2.png)

A few things to work on here. First, let’s move all of this code into a function called generateArtistSong.

```
def generateArtistSong(name):
    songs_array = webScrapeLyrics(name)
    m = MarkovLyrics()
    # Populate the markov chain using all 10 songs
    for song in songs_array:
        # Recall that each song contains an array of lyrics
        m.populateMarkovChain(song)
    return m.generateLyrics()
 
# Our home route
@app.route('/')
def lyricsGenerator():
    print(generateArtistSong("Kendrick Lamar"))
    return render_template('home.html')
```

Second, let’s fix our code so that rather than generating lyrics by Kendric Lamar every time, we’ll generate lyrics by whoever the user specifies in the input field. In home.html, modify the form tag as follows:
```
    <form action="{{ url_for('lyricsGenerator') }}" method="post">
```
Now, whenever we click the submit button on the website, the form data will get sent to lyricsGenerator in app.py.

In our app.py, we will have lyricsGenerator listen to both get requests and post requests. If it receives a post request, that means the user has clicked the “generate lyrics” button. When that happens, call the generateArtistSong method and store the result as the variable song. Then, pass this result to home.html.

```
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
        print(song)
    return render_template('home.html', song=song)
 
 
 
if __name__ == '__main__':
    app.run()
```
In home.html, we want to display this song, so let’s put it in a paragraph:
```
<body>
    <h1>Welcome to Lyrics Generator!</h1>
    <p>Here, you can generate lyrics by the artist of your choice!</p>
    <form action="{{ url_for('lyricsGenerator') }}" method="post">
        <input type="text" id="search" name="search" placeholder="Search for an artist...">
        <input type="submit" value="Generate Lyrics">
    </form>
    <p>{{song}}</p>
</body>
```
If we search for a random artist, we get the following: 

![image](https://user-images.githubusercontent.com/44158788/92676541-c38b1900-f2ef-11ea-8a2c-af2bc5feec22.png)

Getting close! The branch up to this point can be found in branch 4: https://github.com/darrenzhang2000/lyrics-generator/tree/branch4

Now let’s add some newlines. Previously, for simplicity, we replaced \n with space in lyrics.py. Instead, let’s replace it with “ NEWLINE “:
```
def webScrapeLyrics(name):
    arr = getLyricsArray("Kendrick Lamar")
    songs_lyrics = []
    for url in arr:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        lyrics_div = soup.find(class_="lyrics")
        lyrics_links = lyrics_div.find_all('a')
        current_lyrics = []
        for link in lyrics_links:
            if len(link.text) > 0 and link.text[0] != "[":
                text = link.text.replace("\n", " NEWLINE ") #ADDED THIS
                #text = link.text.replace("\n", " ")
                current_lyrics.append(text)
        songs_lyrics.append(current_lyrics)
    return songs_lyrics
 ```
In the generateArtistSong function in app.py, once we generate the song, let’s split the song into lines.
```
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
```
In the home route, rather than passing in the song, pass in an array of lines:
```
# Our home route
@app.route('/', methods = ['GET', 'POST'])
def lyricsGenerator():
    lines = []
    if request.method == 'POST':
        artist = request.form['search']
        lines = generateArtistSong(artist)
    return render_template('home.html', lines=lines)
```
Lastly, in home.html, we want to loop through the list of lines and display each line as on a new paragraph.
```
<body>
    <h1>Welcome to Lyrics Generator!</h1>
    <p>Here, you can generate lyrics by the artist of your choice!</p>
    <form action="{{ url_for('lyricsGenerator') }}" method="post">
        <input type="text" id="search" name="search" placeholder="Search for an artist...">
        <input type="submit" value="Generate Lyrics">
    </form>
    {% for line in lines %}
        <p>{{line}}</p>
    {% endfor %}
</body>
```
![image](https://user-images.githubusercontent.com/44158788/92676613-f2a18a80-f2ef-11ea-9412-dff254cd30fd.png)

The code for this section can be found in branch5: https://github.com/darrenzhang2000/lyrics-generator/tree/branch5
### Styling
To conclude this tutorial, let’s add some styling. 
Create a static folder and in it, create a styles folder. Inside the styles folder, create home.css.

Inside home.html, add the href to the css file.
```
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='styles/home.css') }}">
    <title>Document</title>
</head>
```

Copy and paste this home.css file. Feel free to edit it however you like.

```
#form {
    font-family: 'sans-serif';
    font-size: 24px;
}
 
#submit{
    color: white;
    background-color: #fa8072;
    padding: 5px 20px;
    border-radius: 5px;
    margin-top: 20px;
}
 
#lyrics {
    background-color:  #f0f5f5;
    padding: 5px 20px;
    border: 2px solid red;
    border-radius: 5px;
    margin-top: 20px;
    margin-left: 20%;
    margin-right: 20%;
}
 
body {
    text-align: center;
    background-color: #fcff88;
    font-family: 'Trocchi', serif; 
    font-weight: normal; 
    line-height: 48px; 
}
 
h1 { 
    color: #7c795d; 
    font-size: 45px; 
    margin: 0;
    font-weight: normal;
}
h6 {
    color: #7c795d; 
    font-size: 24px; 
    margin: 0;
    font-weight: normal;
}
 
p {
    color: #7c795d; 
    font-size: 16px; 
    margin: 0;
}
```

Here is the final code:
https://github.com/darrenzhang2000/lyrics-generator

### Conclusion:
And there you have it! I hope you enjoyed this tutorial. If you enjoyed it, please leave a star on my GitHub project. :)
