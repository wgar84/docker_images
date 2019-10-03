FROM base

USER root

COPY chromedriver /opt

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt
RUN rm requirements.txt

RUN apt-get -y install \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    chromium \
    chromium-driver

USER jovyan
WORKDIR /home/jovyan/app

# nltk stuff
RUN python -m nltk.downloader \
    rslp \
    averaged_perceptron_tagger \
    floresta \
    mac_morpho \
    machado \
    punkt \
    stopwords \
    wordnet \
    words
