import re
import math
from ngram import NGram
input_books = ["book.txt", "book2.txt","book3.txt","book4.txt","book5.txt","book6.txt","book7.txt","book8.txt",
               "book9.txt"]
grammers = [NGram(1,input_books[x]) for x in range(9)]
for ind in range(len(input_books)):
    book = open(input_books[ind], encoding="utf8")
    txt = book.read().split("\n")
    book.close()
    txt = txt[26:]
    txt = txt[:-300]
    last_words = []
    n = 1
    cur_gram = grammers[ind]
    print(len(txt))
    for line in txt:
        words = re.sub("[;'.,\"!?]", " ", line)
        grams = re.sub("[.]", " ", words).split(" ")
        for word in grams:
            if word == "":
                continue
            if word == " ":
                continue
            if word == "*":
                continue
            last_words.insert(0, word)
            if len(last_words) > n:
                last_words.pop()
            cur_gram.add_to_self(last_words)


def normalize(arr):
    sm = sum([x[2] for x in arr])
    for i in range(len(arr)):
        arr[i][2] *= 100.0 / sm
        arr[i][2] = round(arr[i][2],1)
    return arr


def prune(grams):
    alls = []
    for elt in grams[0].dct:
        misses = 2
        for gr in grams:
            if elt not in gr.dct:
                misses -= 1
        if misses >= 0:
            alls.append(elt)
    for elt in alls:
        print(elt)
        for gr in grams:
            if elt in gr.dct:
                del gr.dct[elt]


print(grammers[0].dct)
prune(grammers)
for ind in grammers:
    print([x[2] for x in normalize(ind.compare_to(grammers))])
