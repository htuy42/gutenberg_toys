import random

import re


def normalize_flat_dict(dct):
    # for elt in dct:
    #     dct[elt] *= dct[elt]
    summ = sum([dct[x] for x in dct])
    norm = 1.0 / summ
    for elt in dct:
        dct[elt] *= norm
    return dct

def get_word_from_flat_dct(dct):
    nm = random.random()
    sm = 0
    for elt in dct:
        sm += dct[elt]
        if sm > nm:
            return elt
    print("woopsies")
    return "oops"




class NGram:
    def __init__(self,n,id="noid"):
        self.dct = {}
        self.n = n
        self.id = id
        self.author = "NONEAUTHOR"

    def add_to_self(self,prev_words):
        if len(prev_words) >= self.n:
            words_to_use = prev_words[:self.n]
            #print(words_to_use)
            self.rec_add_to_self(words_to_use,self.dct)

    def rec_add_to_self(self,words,dct):
        word = words.pop()
        #print(word)
        if len(words) == 0:
            dct[word] = dct.get(word,0) + 1
            return dct
        else:
            nxt_dct = dct.get(word,{})
            dct[word] = self.rec_add_to_self(words,nxt_dct)
            return dct


    def compare(self,other):
        slf = sum([self.dct[elt] for elt in self.dct])
        other_s = sum([other.dct[elt] for elt in other.dct])
        score = 0

        for elt in self.dct:
            if elt in other.dct:
                score += self.dct[elt] * other.dct[elt]
        return (score / max(slf,other_s,1)) ** 2


    def compare_to(self,others):
        score = [0] * len(others)
        for i in range(len(others)):
            if self.id == others[i].id:
                score[i] = ["a","a",0]
                continue
            score[i] = [self.author, others[i].author, self.compare(others[i])]
        return score


    def normalize_self(self):
        self.rec_normalize_self(self.n, self.dct)



    def rec_normalize_self(self,n,dct):
        if n == 1:
            return normalize_flat_dict(dct)
        else:
            for elt in dct:
                dct[elt] = self.rec_normalize_self(n-1,dct[elt])
            return dct

    def rec_make_word(self,words,dct):
        if len(words) == 1:
            return get_word_from_flat_dct(dct)
        word = words.pop(0)
        if word not in dct:
            return None
        return self.rec_make_word(words,dct[word])

    def read_in_book(self,book):

        bk_txt = []
        try:
            fbook = open(book)
            bk_txt = fbook.read().split("\n")
        except:
            fbook = open(book,encoding="utf8")
            bk_txt = fbook.read().split("\n")

        fbook.close()
        for line in bk_txt:
            cpy = line[:]
            spl = cpy.split(" ")
            if spl[0] == "Author:":
                self.author = " ".join(spl[1:])
                break

        last_words = []
        for line in bk_txt:
            words = re.sub("[[;'.,?|\"()\-\:]]", " ", line)
            grams = re.sub("[.]", " ", words).split(" ")
            for word in words:
                if word == "":
                    continue
                if word == " ":
                    continue
                if word == "*":
                    continue
                self.add_to_self(last_words)
                last_words.insert(0, word)
                if len(last_words) > self.n:
                    last_words.pop()




    def make_word(self,last_words):
        if len(last_words) < self.n:
            return None
        last_words = last_words[:self.n]
        return self.rec_make_word(last_words,self.dct)

    def prune_as_monograms(self, grammers):
        #this won't work when the ngrams have n other that one. It could easily be reworked to do
        #so but hasn't been needed to thus far
        to_prune = []
        for master in grammers[:20]:
            for word in master.dct:
                may_miss = len(grammers) // 5
                for gram in grammers:
                    if word not in gram.dct:
                        may_miss -= 1
                if may_miss > 0:
                    to_prune.append(word)
        for word in to_prune:
            for gram in grammers:
                if word in gram.dct:
                    del gram.dct[word]
