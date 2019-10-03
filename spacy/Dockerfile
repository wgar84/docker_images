FROM nvidia/cuda:10.1-cudnn7-runtime-ubuntu18.04

WORKDIR /app

RUN apt-get -y update --fix-missing

RUN apt-get -y install python3 python3-dev python3-numpy python3-pip locales

COPY requirements.txt .

RUN python3 -m pip install --no-cache-dir -r requirements.txt

RUN python3 -m spacy download pt

RUN mkdir /db

ENV PYTHONPATH="/db:${PYTHONPATH}"

RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=en_US.UTF-8

ENV LANG en_US.UTF-8

RUN useradd -ms /bin/bash -u 1001 jovyan

USER jovyan

WORKDIR /home/jovyan/app

RUN jupyter notebook --generate-config

RUN echo \
    "c.NotebookApp.token = '4fcbc72db3dadfc4585c374a5c83b566b9a86944b1489e79'" \
    >> /home/jovyan/.jupyter/jupyter_notebook_config.py

RUN echo \
    "c.NotebookApp.password = u'sha1:0bff055a03ce:c09cde8bab532481515d631285948252f72e8cc5'" \
    >> /home/jovyan/.jupyter/jupyter_notebook_config.py

RUN python3 -m nltk.downloader \
    rslp \
    averaged_perceptron_tagger \
    floresta \
    mac_morpho \
    machado \
    punkt \
    stopwords \
    wordnet \
    words
