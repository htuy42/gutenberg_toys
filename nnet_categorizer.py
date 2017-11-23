import json
import random

import pickle
from PyDictionary import PyDictionary
from vocabulary.vocabulary import Vocabulary as vb
from time import time

import tensorflow as tf
import re

from story_mimmicker import normalize_flat_dict

all_ids = pickle.load(open("ids.txt","rb"))
# all_ids = {}

print(all_ids)

print(all_ids)
types = set()
for elt in all_ids:
    types.add(all_ids[elt])
print(len(types))
b_size = 100
num_words_to_learn_about = 35

all_word_types = {}

def to_ids(words):
    return [all_ids[x] for x in words]


def get_word_set(book_words):
    done = False
    while not done:
        start = random.randint(0, len(book_words) - num_words_to_learn_about - 300)
        did_frst = False
        for ind in range(start,len(book_words)):
            # print(book_words[ind])
            if book_words[ind] == "endtag123":
                if did_frst:
                    end = ind
                    done = True
                    break
                else:
                    did_frst = True
                    start = ind
                    # done = True
        start += 1
    lst = []
    for x in range(start,end):
        lst.append(book_words[x])
    while len(lst) < num_words_to_learn_about:
        lst.append("ebook")
    if len(lst) > num_words_to_learn_about:
        lst = lst[:num_words_to_learn_about]
    return to_ids(lst)


def parse_in_ids(all_books):
    cur_id = 0

    words_idd = 0
    alls = set()
    for book in all_books:
        for word in book[0]:
            alls.add(word)
    print(len(alls))

    for book in all_books:
        for word in book[0]:
            if word not in all_ids:
                if words_idd % 100 == 0:
                    print("ID'd the first " + str(words_idd) + " words")
                words_idd += 1
                try:
                    def_of_word = vb.part_of_speech(word)
                    if def_of_word is None or def_of_word is False:
                        all_ids[word] = -1
                        continue
                    def_of_word = json.loads(def_of_word)
                except:
                    def_of_word = [{"text":None}]
                for elt in def_of_word:
                    types = elt['text']
                    break
                if types in all_word_types:
                    all_ids[word] = all_word_types[types]
                else:
                    all_word_types[types] = cur_id
                    cur_id += 1
                    all_ids[word] = all_word_types[types]
    pickle.dump(all_ids, open("ids.txt","wb"))
    try:
        pickle.dump(all_ids,"ids.txt")
    except:
        print("didn't work")
    print(len(all_ids))
    print(all_ids)

done_authors = set()

def read_in_all_books(book_ids):
    all_books = []
    book_id = 0

    for id in book_ids:
        try:
            f_book = open(id)
        except:
            f_book = open(id, encoding="utf8")
        txt = f_book.read().split("\n")
        aut = ""
        for line in txt:
            cpy = line[:]
            spl = cpy.split(" ")
            if spl[0] == "Author:":
                aut = " ".join(spl[1:])
                break
        if aut in done_authors:
            continue
        done_authors.add(aut)
        f_book.close()
        all_txt = []
        for line in txt:
            words = re.sub("[[',\"()\-\:]]", " ", line)
            grams = re.sub("[.?!]", " endtag123 ", words).split(" ")
            all_txt += [x.lower() for x in grams]
        all_txt = all_txt[2000:]
        all_books.append((all_txt, book_id))
        book_id += 1
    return all_books


def produce_batch_of_qs_and_as(all_books, batch_size):
    batch_ins = []
    batch_ans = []
    for x in range(batch_size):
        to_use_ind = random.randint(0, len(all_books) - 1)
        to_use = all_books[to_use_ind]
        batch_ins.append(get_word_set(to_use[0]))
        flat_hot = [0] * num_bks
        flat_hot[to_use[1]] = 1
        batch_ans.append(flat_hot)
    return batch_ins, batch_ans


all_ids = normalize_flat_dict(all_ids)


to_read = ["book.txt", "book4.txt", "book8.txt"]

complete_book_list = read_in_all_books(to_read)
parse_in_ids(complete_book_list)
num_bks = len(complete_book_list)

txt = tf.placeholder(tf.float64, [b_size, num_words_to_learn_about])
ans = tf.placeholder(tf.float64, [b_size, num_bks])

U = tf.Variable(tf.random_normal([num_words_to_learn_about, 1000], stddev=.1, dtype=tf.float64), dtype=tf.float64)
bU = tf.Variable(tf.random_normal([1000], stddev=.1, dtype=tf.float64), dtype=tf.float64)
V = tf.Variable(tf.random_normal([1000, num_bks], stddev=.1, dtype=tf.float64), dtype=tf.float64)
bV = tf.Variable(tf.random_normal([num_bks], stddev=.1, dtype=tf.float64), dtype=tf.float64)
ll0 = tf.nn.relu((tf.matmul(txt, U) + bU))

prbs = tf.nn.softmax(tf.matmul(tf.nn.relu(tf.matmul(txt, U) + bU), V) + bV)

x_ent = tf.reduce_mean(-tf.reduce_sum(ans * tf.log(prbs), reduction_indices=[1]))
train = tf.train.GradientDescentOptimizer(.1).minimize(x_ent)
numCorrect = tf.equal(tf.argmax(prbs, 1), tf.argmax(ans, 1))
accuracy = tf.reduce_mean(tf.cast(numCorrect, tf.float64))

sess = tf.Session()
sess.run(tf.global_variables_initializer())

t = time()

for i in range(100000):
    if i % 1000 == 0:
        print(str(i / 1000) + "% done")
        nt = time()
        print("Time elapsed: " + str(nt - t) + " seconds")

    txtt, anss = produce_batch_of_qs_and_as(complete_book_list, b_size)
    sess.run(train, feed_dict={txt: txtt, ans: anss})

sumAcc = 0

for x in range(10000):
    txtt, anss = produce_batch_of_qs_and_as(complete_book_list, b_size)
    sumAcc += sess.run(accuracy, feed_dict={txt: txtt, ans: anss})

print("Test Accuracy: %r" % (sumAcc / 10000))
