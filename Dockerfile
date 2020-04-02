FROM pchuang0219/accton_tms_backend_service:base
LABEL MAINTAINER Anber Huang <anber_huang@accton.com>

RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install -y python python3 python-pip python3-pip python-lxml libxml2-dev \
                      docker.io sshpass iputils-ping libxslt-dev git \
                      wget build-essential language-pack-en python3-tk supervisor

# Install differenet version of Python.
# ENV PY_VERSION=3.3.7
# ENV PY_URL="https://www.python.org/ftp/python/$PY_VERSION/Python-$PY_VERSION.tgz"
# ENV PY_DIR="Python-$PY_VERSION"
# # Download Python
# RUN wget "$PY_URL"
# # Extract it
# RUN tar -xvf "$PY_DIR.tgz" -C /opt && rm -f "$PY_DIR.tgz"
# # Link the headers
# RUN ln -s "/opt/$PY_DIR/Include" /usr/include/python3.4
# # Change to the directory
# WORKDIR "/opt/$PY_DIR"
# # Configure and make and install it
# RUN ./configure && make && make install
# RUN apt-get install -y python3-pip

# Install python-docx package for generate Word report.
# RUN git clone https://github.com/python-openxml/python-docx
# WORKDIR python-docx/
# RUN python setup.py install

ADD . /source/flask-app
WORKDIR /source/flask-app/Execute

RUN pip3 install --upgrade pip
RUN pip3 install -r ../environment/requirements.txt

ENV PYTHONIOENCODING=UTF-8
ENV LANG='en_US.utf8'
ENV LC_ALL='en_US.utf8'

COPY ../environment/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
EXPOSE 8000
CMD ["/usr/bin/supervisord","-n"]