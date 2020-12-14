FROM snakepacker/python:all as builder
MAINTAINER vnkrtv

RUN python3.7 -m venv /usr/share/python3/venv
RUN /usr/share/python3/venv/bin/pip install -U pip

COPY requirements.txt /mnt/
RUN /usr/share/python3/venv/bin/pip install -Ur /mnt/requirements.txt

FROM snakepacker/python:3.7 as api

COPY --from=builder /usr/share/python3/venv /usr/share/python3/venv
RUN  /usr/share/python3/venv/bin/python -m playwright install
RUN apt-get update -y \
 && apt-get install -y libglib2.0-0\
          libsoup2.4-1\
          libcairo2\
          libgtk-3-0\
          libgl1\
          libegl1\
          libnotify4\
          libgdk-pixbuf2.0-0\
          libvpx6\
          libopus0\
          libxml2\
          libicu66\
          libxslt1.1\
          libwoff1\
          libfontconfig1\
          libfreetype6\
          libharfbuzz0b\
          libharfbuzz-icu0\
          libgstreamer-plugins-base1.0-0\
          libgstreamer1.0-0\
          libgstreamer-gl1.0-0\
          libgstreamer-plugins-bad1.0-0\
          libjpeg-turbo8\
          libpng16-16\
          libopenjp2-7\
          libwebpdemux2\
          libwebp6\
          libenchant1c2a\
          libsecret-1-0\
          libhyphen0\
          libx11-6\
          libxcomposite1\
          libxdamage1\
          libwayland-server0\
          libwayland-egl1\
          libwayland-client0\
          libpango-1.0-0\
          libatk1.0-0\
          libxkbcommon0\
          libepoxy0\
          libatk-bridge2.0-0\
          libgles2\
          gstreamer1.0-libav
COPY . /usr/share/python3/

ENTRYPOINT ["/usr/share/python3/venv/bin/python3.7", "/usr/share/python3/main.py"]