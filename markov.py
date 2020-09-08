from random import randint

class MarkovLyrics:
    def __init__(self):
        # A dictionary containing phrases (each phrase contains self.order number of words)
        # Example 
        # self.chain = {
        #   "baby": [plays, sleeps, crawls, sleeps],
        #   "plays": [toy, food],
        # }
        self.chain = {}

        self.order = 1 # The number of words in each phrase

    def populateMarkovChain(self, lyrics):
        for line in lyrics:
            words = line.split(" ")
            # For every possible starting index of the phrase  
            for i in range(len(words) - self.order):
                phrase = ""
                # Builds phrase with the first j words
                for j in range(self.order): 
                    phrase += words[i + j]
                # If the phrase is already in the dictionary, 
                # append next_word to the list of possible words
                # for the phrase
                if phrase in self.chain:
                    next_word = words[i + self.order]
                    self.chain[phrase].append(next_word)
                # First time this phrase occurs
                # next_word is the only possible next word right now
                else:
                    next_word = words[i + self.order]
                    self.chain[phrase] = [next_word]


    def generateLyrics(self, lyrics_length=500):
        n = len(m.chain)
        m_dict = m.chain

        # Choose a random starting word
        start_index = randint(0, n - self.order)
        l = list(m.chain)
        cur_word = l[start_index]

        # result string
        res = cur_word + " "

        for _ in range(lyrics_length):
            if cur_word not in m.chain:
                next_index = randint(0, len(m.chain) - 1)
                l = list(m.chain)
                cur_word = l[next_index]
            else:
                possible_words = m_dict[cur_word]
                index = randint(0, len(possible_words) - 1)
                next_word = possible_words[index]
                res += next_word + ' '
                cur_word = next_word
        return res

m = MarkovLyrics()
dummydata = ['''Interference, it's such a receipt, huh?

I want

I drink liquor on they mom while she wanna hear not your ways deceitful

Because you got a gang member, you's a destruction mode if phil jackson came from the same niggas just what happens on full, that's the one hand, I been ready, my metropolis, feel a song, alright

Tapped in the blacker the weekend

Show you want everything black, I know you killed

You ain't good game, homie, you want

Would fight less and right

And funeral faces

James bonding with''']
# dummydata = ['cat dog cat cat cat dog bat fat dat quat']
m.populateMarkovChain(dummydata)

print(m.generateLyrics())
# print(m.chain)