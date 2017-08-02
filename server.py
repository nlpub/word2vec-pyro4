#!/usr/bin/env python

import argparse
from gensim.models import KeyedVectors
import Pyro4

parser = argparse.ArgumentParser(description='Word Vectors Served via Pyro4.', add_help=False)
parser.add_argument('--w2v', required=True, type=argparse.FileType('rb'))
parser.add_argument('-h', '--host', default='', type=str)
parser.add_argument('-p', '--port', default=9090, type=int)
args = parser.parse_args()

Pyro4.config.SERIALIZERS_ACCEPTED = {'pickle'}
Pyro4.config.SERIALIZER = 'pickle'

PyroVectors = Pyro4.expose(KeyedVectors)

w2v = PyroVectors.load_word2vec_format(args.w2v, binary=True, unicode_errors='ignore')
w2v.init_sims(replace=True)

daemon = Pyro4.Daemon(host=args.host, port=args.port)
print(daemon.register(w2v, 'w2v'))
daemon.requestLoop()
