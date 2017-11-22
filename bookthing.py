import random
import re
book = open("book.txt", encoding="utf8")
book_text = book.read().split("\n")
counts = {}
bi_grams = {}
tri_grams = {}
mono_grams = {}
last = "begin"
last_2 = "begin"

def add_to_flat_dict(dct,word):
    dct[word] = dct.get(word,0) + 1

for line in book_text:
    words = re.sub("[;'.,]"," ",line)
    grams = re.sub("[.]"," END",words).split(" ")
    for word in grams:
        dct = bi_grams.get(last,{})
        add_to_flat_dict(dct,word)
        bi_grams[last] = dct
        dct_2 = tri_grams.get(last_2,{})
        dct = dct_2.get(last,{})
        add_to_flat_dict(dct,word)
        dct_2[last] = dct
        tri_grams[last_2] = dct_2
        add_to_flat_dict(mono_grams,word)
        last_2 = last
        last = word

def normalize_flat_dict(dct):
    summ = sum([dct[x] for x in dct])
    norm = 1.0 / summ
    for elt in dct:
        dct[elt] *= norm
    return dct

mono_grams = normalize_flat_dict(mono_grams)
for elt in bi_grams:
    bi_grams[elt] = normalize_flat_dict(bi_grams[elt])

for elt in tri_grams:
    bi_dct = tri_grams[elt]
    for selt in bi_dct:
        bi_dct[selt] = normalize_flat_dict(bi_dct[selt])
    tri_grams[elt] = bi_dct

new_story = ""

def get_word_from_flat_dct(dct):
    nm = random.random()
    sm = 0
    for elt in dct:
        sm += dct[elt]
        if sm > nm:
            return elt
    print("woopsies")
    return "oops"

last_2 = "begin"
last = "begin"
for x in range(2000):
    if x % 15 == 0 and x != 0:
        new_story += "\n"
    if last_2 in tri_grams:
        if last in tri_grams[last_2]:
            r = get_word_from_flat_dct(tri_grams[last_2][last])
            new_story += r
            new_story += " "
            last_2 = last
            last = r
            continue
    if last in bi_grams:
        r = get_word_from_flat_dct(bi_grams[last])
        new_story += r
        new_story += " "
        last_2 = last
        last = r
    r = get_word_from_flat_dct(mono_grams)
    new_story += r
    new_story += " "
    last_2 = last
    last = r


new_story_split = new_story.split("\n")
for elt in new_story_split:
    print(elt)