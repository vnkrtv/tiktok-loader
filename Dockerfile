FROM snakepacker/python:all as builder
MAINTAINER vnkrtv

RUN python3.7 -m venv /usr/share/python3/venv
RUN /usr/share/python3/venv/bin/pip install -U pip

COPY requirements.txt /mnt/
RUN /usr/share/python3/venv/bin/pip install -Ur /mnt/requirements.txt \
 && /usr/share/python3/venv/bin/python -m playwright install

FROM snakepacker/python:3.7 as api

COPY --from=builder /usr/share/python3/venv /usr/share/python3/venv
COPY . /usr/share/python3/

ENTRYPOINT ["/usr/share/python3/venv/bin/python", "/usr/share/python3/main.py"]