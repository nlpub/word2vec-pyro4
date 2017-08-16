FROM continuumio/miniconda3

MAINTAINER Dmitry Ustalov <dmitry.ustalov@gmail.com>

EXPOSE 9090

RUN conda install gensim && pip install Pyro4 && conda clean -a

WORKDIR /usr/src/app

COPY server.py .

USER nobody

CMD ["python", "server.py", "--w2v", "/usr/src/app/w2v.bin"]
