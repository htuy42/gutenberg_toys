import os

from ngram import NGram

books = []
for root, dirs, files in os.walk("unzipped_books", topdown=False):
    for name in files:
        books.append("unzipped_books/" + name)
    for name in dirs:
        di = "unzipped_books/"+name
        for sf in os.listdir(di):
            if "unzipped_books/" + sf in books:
                books.remove("unzipped_books/" + sf)
            books.append(di + "/" + sf)

# books = books[:10]

grammers = [NGram(1,x) for x in books]

for ind in range(len(books)):
    if ind % 10 == 0:
        print(ind)
    grammers[ind].read_in_book(books[ind])

grammers[0].prune_as_monograms(grammers)

def normalize(arr):
    sm = sum([x[2] for x in arr])
    for i in range(len(arr)):
        arr[i][2] *= 100.0 / max(sm,1.0)
        arr[i][2] = round(arr[i][2],1)
    return arr

results = open("similarity_results.txt","w")

most_sims = []
author_dicts = {}
for gram in grammers:
    comparisons = normalize(gram.compare_to(grammers))
    srted = sorted(comparisons,key=lambda x: x[2],reverse=True)
    results.write("Current book's author: " + gram.author)
    results.write("Current book: " + gram.id)
    results.write("\n")
    results.write("10 most similar other books: ")
    results.write("\n")
    results.write(",".join([x[1] for x in srted[:10]]))
    results.write("\n")
    for elt in srted[:8]:
        key = (gram.author,elt[1])
        if gram.author == elt[1]:
            continue
        if gram.author == "Various" or gram.author == "NONEAUTHOR":
            continue
        if elt[1] == "Various" or elt[1] == "NONEAUTHOR":
            continue
        author_dicts[key] = author_dicts.get(key,0) + 1

    print([x[2] for x in normalize(gram.compare_to(grammers))])
    for elt in comparisons:
        most_sims.append((elt[2],elt[1],elt[0]))
    most_sims = sorted(most_sims,reverse=True)
    most_sims = most_sims[:50]

results.write("Most similar pairings of books overall: ")
results.write("\n".join([":".join([str(y) for y in x]) for x in most_sims]))

results.close()

cates = open("category_results.txt","w")
cate_lst = []
for elt in author_dicts:
    if author_dicts[elt] == 1:
        continue
    cate_lst.append((author_dicts[elt],elt))

cate_lst = sorted(cate_lst,reverse=True)
print(author_dicts)
print(cate_lst)
for elt in cate_lst:
    cates.write(str(elt[1][0]) + " " + str(elt[1][1]) +" : " +str(elt[0]) + "\n")

cates.close()