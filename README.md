# Word Vectors Served via Pyro4.

This is a simple network service that serves the [Gensim]'s `KeyedVectors` via [Pyro4].

[Gensim]: https://radimrehurek.com/gensim/
[Pyro4]: https://pythonhosted.org/Pyro4/

[![Dependency Status][gemnasium_badge]][gemnasium_link] [![Docker Hub][docker_badge]][docker_link]

[gemnasium_badge]: https://gemnasium.com/nlpub/word2vec-pyro4.svg
[gemnasium_link]: https://gemnasium.com/nlpub/word2vec-pyro4
[docker_badge]: https://img.shields.io/docker/pulls/nlpub/word2vec-pyro4.svg
[docker_link]: https://hub.docker.com/r/nlpub/word2vec-pyro4/

## Running

```shell
$ ./server.py
usage: server.py [--id ID] [--no-sims] [-h HOST] [-p PORT] w2v
```

The only mandatory parameter, `w2v`, specifies the path to the word vectors in the [word2vec](https://code.google.com/archive/p/word2vec/) format. By default, the server listens to any network interface on the port 9090.

For instance, the following pre-trained vectors are available:

* English: [Google News](https://code.google.com/archive/p/word2vec/), [GloVe](https://nlp.stanford.edu/projects/glove/), [fastText](https://github.com/facebookresearch/fastText/blob/master/pretrained-vectors.md);
* Russian: [Russian Distributional Thesaurus](http://russe.nlpub.ru/downloads/#rdt-russian-distributional-thesaurus), [RusVectōrēs](http://rusvectores.org/ru/).

Note that the Docker image is based on [Anaconda 3](https://hub.docker.com/r/continuumio/miniconda3/) for performance reasons. The image is designed under the assumption that the vectors are mounted as `/usr/src/app/w2v.bin`.

## Accessing

```python
import Pyro4

Pyro4.config.SERIALIZER = 'pickle' # see the Disclaimer

w2v = Pyro4.Proxy('PYRO:w2v@localhost:9090')

w2v.word_vec('cat') # => array([…], dtype=float32)
```

## Disclaimer

Note that this service should be running in a trusted environment since it uses the `pickle` serializer to handle the [NumPy](http://www.numpy.org/) arrays. This makes the system extremely vulnerable and even allows arbitrary code execution, which is [not recommended](http://pythonhosted.org/Pyro4/tipstricks.html#pyro-and-numpy) by the Pyro4 developers.

## Copyright

Copyright (c) 2017 [Dmitry Ustalov]. See LICENSE for details.

[Dmitry Ustalov]: https://ustalov.com/
