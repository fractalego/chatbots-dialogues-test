from gensim import utils
from gensim.models.doc2vec import TaggedDocument
from gensim.models import Doc2Vec
from random import shuffle
import nltk

path = 'ordered_lines.txt'

WINDOW_SIZE = 20

lines = [line for line in open(path, encoding="ISO-8859-1").readlines()]


class LabeledLineSentence(object):
    def __init__(self, sources):
        self.sources = sources

        flipped = {}

        # make sure that keys are unique
        for key, value in sources.items():
            if value not in flipped:
                flipped[value] = [key]
            else:
                raise Exception('Non-unique prefix encountered')

    def to_array(self):
        self.sentences = []
        for source, prefix in self.sources.items():
            text = source
            tokenizer = nltk.tokenize.TweetTokenizer()
            words = tokenizer.tokenize(utils.to_unicode(text))
            words = [word.lower() for word in words]
            self.sentences.append(TaggedDocument(words=words, tags=[prefix]))
        return self.sentences

    def sentences_perm(self):
        shuffle(self.sentences)
        return self.sentences


sources = {}

for i in range(len(lines)):
    line = lines[i]
    ident = str(i)
    sources[line] = 'LINES_' + str(ident)

sentences = LabeledLineSentence(sources)

model = Doc2Vec(window=WINDOW_SIZE, size=100, sample=1e-4, negative=5, workers=4, dm=0)
model.build_vocab(sentences.to_array())

for epoch in range(0, 151):
    print('Training epoch ' + str(epoch) + '.')
    model.train(sentences.sentences_perm(), total_examples=model.corpus_count, epochs=model.iter)
    if epoch % 50 == 0:
        model.save('./lines-' + str(epoch) + '.d2v')
