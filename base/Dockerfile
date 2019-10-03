FROM python:3.7.4-buster

MAINTAINER Guilherme Garcia <pectinidae@gmail.com>

# R base
COPY jranke.asc .
RUN echo 'deb http://cloud.r-project.org/bin/linux/debian buster-cran35/' >> /etc/apt/sources.list
RUN apt-key add jranke.asc
RUN apt-get update
RUN apt-get -y install r-base phantomjs
COPY requirements.R .
RUN Rscript -e "source('requirements.R')"
RUN rm requirements.R

# RUN apt-get -y install curl
# RUN curl -sL https://deb.nodesource.com/setup_12.x | bash -
# RUN apt-get -y install nodejs
# RUN npm -g install phantomjs-prebuilt

# bokeh depends on phantomjs
# COPY phantomjs /opt
# ENV PATH="/opt:$PATH"

# python with nbreport support
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY nbclean.txt .
RUN python -m pip install --no-cache-dir -r nbclean.txt
COPY nbreport.txt .
RUN python -m pip install --no-cache-dir -r nbreport.txt
RUN jupyter bundlerextension enable --py nbreport --sys-prefix

ENV PATH="/opt:$PATH"

# R kernels
RUN Rscript -e "IRkernel::installspec(user=FALSE)"

# jupyter config
RUN useradd -ms /bin/bash -u 1001 jovyan
USER jovyan
RUN jupyter notebook --generate-config
RUN echo \
    "c.NotebookApp.token = '4fcbc72db3dadfc4585c374a5c83b566b9a86944b1489e79'" \
    >> /home/jovyan/.jupyter/jupyter_notebook_config.py
RUN echo \
    "c.NotebookApp.password = u'sha1:0bff055a03ce:c09cde8bab532481515d631285948252f72e8cc5'" \
    >> /home/jovyan/.jupyter/jupyter_notebook_config.py
