import random
import re
from ngram import NGram




input_books = ["book.txt", "book2.txt","book3.txt","book4.txt","book5.txt","book6.txt","book7.txt","book8.txt",
               "book9.txt"]

books_texts = []
for elt in input_books:
    book = open(elt,encoding="utf8")
    txt = book.read().split("\n")
    books_texts += txt
    book.close()

last_words = []
n = 3
grammers = [NGram(x) for x in range(1,n)]

print(len(books_texts))

i = 0
sm = 0
for line in books_texts:
    if i % 1000 == 0:
        print(i)
    i += 1
    words = re.sub("[;'.,]"," ",line)
    grams = re.sub("[.]", " ",words).split(" ")
    for word in grams:
        if word == "":
            continue
        if word == " ":
            continue
        if word == "*":
            continue
        for gram in grammers:
            gram.add_to_self(last_words)
        last_words.insert(0,word)
        if len(last_words) > n:
            last_words.pop()

new_story = ""
grammers = list(reversed(grammers))
cnt = {}
for gram in grammers:
    gram.normalize_self()
for x in range(2000):
    if x % 20 == 0 and x is not 0:
        new_story += "\n"
    did = False
    i = 0
    for gram in grammers:
        i += 1
        r = gram.make_word(last_words)
        if r is not None:
            new_story += r + " "
            did = True
            last_words.insert(0, r)
            if len(last_words) > n:
                last_words.pop()
            cnt[i] = cnt.get(i,0) + 1
            break
    if not did:
        print("all failed")

s_story = new_story.split("\n")
for elt in s_story:
    print(elt)

print(cnt)

