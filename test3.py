import itertools
import time
from lsh import cache, minhash 


def shingles(text, char_ngram=5):
    return set(text[head:head + char_ngram] for head in range(0, len(text) - char_ngram))


def jaccard(set_a, set_b):
    intersection = set_a & set_b
    union = set_a | set_b
    return len(intersection) / len(union)


def candidate_duplicates(document_feed, char_ngram=5, seeds=100, bands=10, hashbytes=4):
    char_ngram = 5
    sims = []
    hasher = minhash.MinHasher(seeds=seeds, char_ngram=char_ngram, hashbytes=hashbytes)
    if seeds % bands != 0:
	    raise ValueError('Seeds has to be a multiple of bands. {} % {} != 0'.format(seeds, bands))

    lshcache = cache.Cache(num_bands=bands, hasher=hasher)
    for i_line, line in enumerate(document_feed):
	    line = line.decode('utf8')
	    docid, headline_text = line.split('\t', 1)
	    fingerprint = hasher.fingerprint(headline_text.encode('utf8'))
		
	    # in addition to storing the fingerpring store the line
	    # number and document ID to help analysis later on
	    lshcache.add_fingerprint(fingerprint, doc_id=(i_line, docid))

    candidate_pairs = set()
    for b in lshcache.bins:
	    for bucket_id in b:
		    if len(b[bucket_id]) > 1:
			    pairs_ = set(itertools.combinations(b[bucket_id], r=2))
			    candidate_pairs.update(pairs_)

    return candidate_pairs

hasher = minhash.MinHasher(seeds=100, char_ngram=5, hashbytes=4)

lines = []
start_time = time.time()
with open('dataset.txt', 'rb') as fh:
    # read the first 1000 lines into memory so we can compare them
    for line in itertools.islice(fh, 10000):
        lines.append(line.decode('utf8'))
    
    # reset file pointer and do LSH
    fh.seek(0)
    feed = itertools.islice(fh, 10000)
    candidates = candidate_duplicates(feed, char_ngram=5, seeds=100, bands=10, hashbytes=4)

# go over all the generated candidates comparing their similarities
similarities = []
found = 0
for ((line_a, docid_a), (line_b, docid_b)) in candidates:
    doc_a, doc_b = lines[line_a], lines[line_b]
    shingles_a = shingles(doc_a)
    shingles_b = shingles(doc_b)    
    if jaccard(shingles_a, shingles_b) > 0.9:
        found += 1

print('Number of candidate pairs found: %s' %(len(candidates)))
print('Number of candidates above threshold: %s' %found)
print('It took %s seconds.' %(time.time()-start_time))


