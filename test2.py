import itertools
from lsh import cache, minhash

def shingles(text, char_ngram=5):
    return set(text[head:head + char_ngram] for head in range(0, len(text) - char_ngram))


def jaccard(set_a, set_b):
    intersection = set_a & set_b
    union = set_a | set_b
    return len(intersection) / len(union)


hasher = minhash.MinHasher(seeds=20, char_ngram=5, hashbytes=4)

lines = []

with open('dataset.txt', 'rb') as fh:
    # read the first 1000 lines into memory so we can compare them
    for line in itertools.islice(fh, 1000):
        lines.append(line.decode('utf8'))
    
    # reset file pointer and do LSH
    fh.seek(0)
    feed = itertools.islice(fh, 1000)
    candidates = [((3, '3'), (15, '15')),((9, '9'), (11, '11')), ((35, '35'), (70, '70')), ((77, '77'), (93, '93'))]

# go over all the generated candidates comparing their similarities
similarities = []
for ((line_a, docid_a), (line_b, docid_b)) in candidates:
    doc_a, doc_b = lines[line_a], lines[line_b]
    shingles_a = shingles(lines[line_a])
    shingles_b = shingles(lines[line_b])
    
    jaccard_sim = jaccard(shingles_a, shingles_b)
    fingerprint_a = set(hasher.fingerprint(doc_a.encode('utf8')))
    fingerprint_b = set(hasher.fingerprint(doc_b.encode('utf8')))
    minhash_sim = len(fingerprint_a & fingerprint_b) / len(fingerprint_a | fingerprint_b)
    similarities.append((docid_a, docid_b, jaccard_sim, minhash_sim))

for x in similarities:
    print(x)


