import zipfile
import os
f = 0
s = 0
fs = []
for elt in os.listdir("books"):
    try:
        zip_ref = zipfile.ZipFile("books/" + elt, 'r')
        zip_ref.extractall("unzipped_books")
        zip_ref.close()
        s += 1
    except:
        fs.append(elt)
        f += 1

print("Unzipping done. Succeeded " + str(s) + " out of " + str(f + s) + " file. List of failed files:")
print(" ".join(fs))