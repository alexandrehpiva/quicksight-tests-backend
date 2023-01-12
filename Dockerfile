FROM amazonlinux:2 as python-base

WORKDIR /app
 

# GLOBAL ENVS - # PYTHON
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHON_VERSION=3.10.2 \
    # PIP
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # poetry
    VENV_PATH='/app/.venv/'

# UPDATE CACHE AND INSTALL PACKAGES
RUN yum clean all
RUN yum update -y
RUN yum update -y \
    kernel rust expat curl zlib glibc libgcrypt openldap python libxml2 openssl openssl11
RUN yum install -y \
    make \
    tzdata \
    shadow-utils \
    ca-certificates \
    glibc-langpack-pt.x86_64 \
    # PYTHON INSTALL DEPENDENCIES
    gcc tar wget gzip bzip2-devel openssl11 openssl11-devel libffi libffi-devel \
    # UPDATE CERTIFICATES
    && update-ca-trust \
    # ADD GROUP AND USER
    && groupadd -r appuser && useradd -r -s /bin/false -g appuser appuser \
    # CONFIG YUM
    && sed -i '1!b;s/python/python2.7/' /usr/bin/yum \
    && sed -i '1!b;s/python/python2.7/' /usr/libexec/urlgrabber-ext-down \
    # INSTALL PYTHON
    && wget -O python.tgz "https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz" \
    && tar -xf python.tgz \
    && ./Python-${PYTHON_VERSION}/configure --enable-optimizations --with-ensurepip=install \
    && make -j $(nproc) && make altinstall \
    && rm -rf /app/* \
    # REMOVE PACKAGES
    && yum remove wget tar gcc shadow-utils gzip bzip2-devel openssl11 openssl11-devel vim vim-data -y \
    && yum clean all && rm -rf /var/cache/yum \
    # CONFIG PYTHON
    && rm /usr/bin/python \
    && ln -s /usr/local/bin/python3.10 /usr/bin/python \
    && ln -s /usr/local/bin/pip3.10 /usr/bin/pip \
    # TZ
    && cp /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime && echo "America/Sao_Paulo" > /etc/timezone

FROM python-base as dependencies
 

RUN yum install -y curl gcc gcc-c++ \
    # UPDATE PIP AND INSTALL PYTHON PACKAGES
    && pip install -U pip setuptools wheel poetry

RUN poetry config virtualenvs.in-project true
RUN mkdir .venv && chown appuser:appuser .venv

COPY poetry.lock pyproject.toml ./
 

RUN poetry install --no-dev --no-root
 

FROM python-base as release
 

# https://github.com/dynatrace-oss/OneAgent-SDK-Python-AutoInstrumentation
ENV AUTODYNATRACE_INSTRUMENT_STARLETTE=0 \
    AUTODYNATRACE_INSTRUMENT_SUBPROCESS=0 \
    AUTODYNATRACE_INSTRUMENT_CONCURRENT=1

RUN pip install -U pip poetry
 

# PERMISSIONS
RUN chown -R appuser: /app /etc/ssl/ /home && chmod -R u+rwx /app /etc/ssl/ \
    && chmod a-rwx /usr/bin/env /usr/bin/modutil /usr/bin/echo /usr/bin/chmod /usr/bin/chown /usr/bin/chgrp

COPY --chown=appuser:appuser --from=dependencies $VENV_PATH $VENV_PATH
 

COPY --chown=appuser:appuser . .
 

USER appuser

EXPOSE 8000

CMD ["make", "run"]