from random import randint

class MarkovLyrics:
    def __init__(self):
        self.markov_lyrics = {}
        self.order = 1

    def generateMarkovChain(self, lyrics):
        for line in lyrics:
            words = line.split(" ")
            for i in range(len(words) - self.order):
                phrase = ""
                for j in range(self.order):
                    phrase += words[i + j]
                if phrase in self.markov_lyrics:
                    next_word = words[i + self.order]
                    self.markov_lyrics[phrase].append(next_word)
                else:
                    next_word = words[i + self.order]
                    self.markov_lyrics[phrase] = [next_word]

m = MarkovLyrics()
m.generateMarkovChain(['''Interference, it's such a receipt, huh?

I want

I drink liquor on they mom while she wanna hear not your ways deceitful

Because you got a gang member, you's a destruction mode if phil jackson came from the same niggas just what happens on full, that's the one hand, I been ready, my metropolis, feel a song, alright

Tapped in the blacker the weekend

Show you want everything black, I know you killed

You ain't good game, homie, you want

Would fight less and right

And funeral faces

James bonding with'''])

n = len(m.markov_lyrics)

m_dict = m.markov_lyrics

start_index = randint(0, n)
l = list(m.markov_lyrics)
cur_word = l[start_index]
res = cur_word + " "
for i in range(10):
    possible_words = m_dict[cur_word]
    index = randint(0, len(possible_words) - 1)
    next_word = possible_words[index]
    res += next_word + ' '
    cur_word = next_word
print(res)