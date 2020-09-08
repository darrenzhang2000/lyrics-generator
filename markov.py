from random import randint

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

    # length is the length so the song we generate
    def generateLyrics(self, length=500):
            n = len(self.chain)
    
            # Choose a random starting word
            start_index = randint(0, n - 1)
            keys = list(self.chain.keys())
            cur_word = keys[start_index]
    
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

