from gensim.models import Doc2Vec
import numpy as np
import matplotlib.pyplot as plt
from bhtsne import tsne

ZERO = 0


def get_vector(i, vocab_size):
    vect = [ZERO] * vocab_size
    vect[i] = 1.
    return vect


model = Doc2Vec.load('./lines-150.d2v')

doc_vectors = []
doc_ids = []
doc_idents = list(model.docvecs.doctags.keys())
for ident in doc_idents:
    doc_vectors.append(np.array(model.docvecs[ident], dtype=np.float64))
    doc_ids.append(ident)

MAX_VECTORS = len(doc_vectors)
doc_vectors = np.array(doc_vectors[:MAX_VECTORS])
doc_ids = doc_ids[:MAX_VECTORS]

semantic_doc_vectors = np.array(doc_vectors)
projected = tsne(semantic_doc_vectors, dimensions=2, perplexity=5)

x = np.array(projected[:, 0])
y = np.array(projected[:, 1])
fig, ax = plt.subplots()
ax.scatter(x, y, marker='.')
plt.show()

file = open('results/tsne_coordinates.txt', 'w')
matching_labels = 0
tot_labels = 0
for ident, xi, yi in zip(doc_ids, x, y):
    file.write(str(xi) + ' '
               + str(yi) + ' '
               + str(ident) + '\n')
