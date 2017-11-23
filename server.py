#!/usr/bin/env python

import argparse
from gensim.models import KeyedVectors
import Pyro4

parser = argparse.ArgumentParser(description='Word Vectors Served via Pyro4.', add_help=False)
parser.add_argument('--id',  default='w2v', type=str)
parser.add_argument('-h', '--host', default='', type=str)
parser.add_argument('-p', '--port', default=9090, type=int)
parser.add_argument('w2v', type=argparse.FileType('rb'))
args = parser.parse_args()

Pyro4.config.SERIALIZERS_ACCEPTED = {'pickle'}
Pyro4.config.SERIALIZER = 'pickle'

wv = KeyedVectors.load_word2vec_format(args.w2v, binary=True, unicode_errors='ignore')
wv.init_sims(replace=True)

# This is an adapter for the KeyedVectors class.
# Unfortunately, it is not possible to expose the __getitem__ method.
class PyroVectors:
    def __init__(self, wv):
        self.wv = wv

    @Pyro4.expose
    def word_vec(self, word, use_norm=False):
        return self.wv.word_vec(word, use_norm)

    @Pyro4.expose
    def words_vec(self, words, use_norm=False):
        return {word: self.wv.word_vec(word, use_norm) for word in words if word in self.wv}

    @Pyro4.expose
    def most_similar(self, positive=[], negative=[], topn=10, restrict_vocab=None, indexer=None):
        return self.wv.most_similar(positive, negative, topn, restrict_vocab, indexer)

    @Pyro4.expose
    def wmdistance(self, document1, document2):
        return self.wmdistance(document1, document2)

    @Pyro4.expose
    def most_similar_cosmul(self, positive=[], negative=[], topn=10):
        return self.wv.most_similar_cosmul(positive, negative, topn)

    @Pyro4.expose
    def similar_by_word(self, word, topn=10, restrict_vocab=None):
        return self.wv.similar_by_word()

    @Pyro4.expose
    def similar_by_vector(self, vector, topn=10, restrict_vocab=None):
        return self.wv.similar_by_vector(word, topn, restrict_vocab)

    @Pyro4.expose
    def doesnt_match(self, words):
        return self.wv.doesnt_match(vector, topn, restrict_vocab)

    @Pyro4.expose
    def similarity(self, w1, w2):
        return self.wv.similarity(w1, w2)

    @Pyro4.expose
    def n_similarity(self, ws1, ws2):
        return self.wv.n_similarity(ws1, ws2)

    @Pyro4.expose
    @property
    def syn0(self):
        return self.wv.syn0

    @Pyro4.expose
    @property
    def syn0norm(self):
        return self.wv.syn0norm

    @Pyro4.expose
    @property
    def vocab(self):
        return self.wv.vocab

    @Pyro4.expose
    @property
    def index2word(self):
        return self.wv.index2word

    @Pyro4.expose
    @property
    def vector_size(self):
        return self.wv.vector_size

daemon = Pyro4.Daemon(host=args.host, port=args.port)
print(daemon.register(PyroVectors(wv), args.id), flush=True)
daemon.requestLoop()
