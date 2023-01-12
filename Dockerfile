# Dockerfile for building a Python 3.10.2 image for Amazon Linux 2 and install pachages with poetry


FROM amazonlinux:2 as python-base


WORKDIR /app


# GLOBAL ENVS

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHON_VERSION=3.10.2
ENV PYTHON_PIP_VERSION=21.3.1
ENV PYTHON_PATH=/usr/local/bin/python3
ENV PYTHON_PIP_PATH=/usr/local/bin/pip3
ENV PYTHON_PIPENV_PATH=/usr/local/bin/pipenv
ENV PYTHON_POETRY_PATH=/usr/local/bin/poetry


# SSL config

# COPY serasa_certs.crt /app/serasa_certs.crt
# RUN cat /app/serasa_certs.crt >> /etc/pki/tls/certs/ca-bundle.crt
# RUN echo "sslverify=false" >> /etc/yum.conf


# Install Python

RUN yum install -y \
  gcc \
  gcc-c++ \
  make \
  openssl-devel \
  bzip2-devel \
  libffi-devel \
  zlib-devel \
  readline-devel \
  sqlite-devel \
  wget \
  tar \
  xz \
  && yum clean all \
  && rm -rf /var/cache/yum


RUN wget https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz \
  && tar -xvf Python-${PYTHON_VERSION}.tgz \
  && cd Python-${PYTHON_VERSION} \
  && ./configure --enable-optimizations \
  && make altinstall \
  && cd .. \
  && rm -rf Python-${PYTHON_VERSION} \
  && rm -rf Python-${PYTHON_VERSION}.tgz


# Install pip

RUN ${PYTHON_PATH} -m ensurepip \
&& ${PYTHON_PIP_PATH} install --upgrade pip==${PYTHON_PIP_VERSION}


# Install pipenv

RUN ${PYTHON_PIP_PATH} install pipenv==2021.11.23


# Install poetry

RUN ${PYTHON_PIP_PATH} install poetry==1.1.11


# Install packages

COPY pyproject.toml poetry.lock ./
RUN ${PYTHON_POETRY_PATH} install --no-dev


# Copy source code

COPY . .


# Run app

CMD ["make", "run"]


# Path: Dockerfile