import itertools
import time


def get_shingles(text, char_ngram=5):
    return set(text[head:head + char_ngram] for head in range(0, len(text) - char_ngram))


def jaccard(set_a, set_b):
    intersection = set_a & set_b
    union = set_a | set_b
    return len(intersection) / len(union)

shingles = []
start_time = time.time()
with open('dataset.txt', 'r') as fh:
    for i_line, line in enumerate(fh):
        if i_line > 100:
            break
        document_id, article_text = line.split('\t', maxsplit=1)
        shingles.append(get_shingles(article_text.lower()))


duplicates = []
for i_doc in range(len(shingles)):
    for j_doc in range(i_doc + 1, len(shingles)):
        jaccard_similarity = jaccard(shingles[i_doc], shingles[j_doc])
        is_duplicate = jaccard_similarity >= 0.40
        if is_duplicate:
            duplicates.append((i_doc, j_doc, jaccard_similarity))

print('It took %s seconds.' %(time.time()-start_time))
print(len(duplicates))

