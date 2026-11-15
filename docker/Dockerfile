FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    binutils \
    python3-tk \
    portaudio19-dev \
    gcc \
    libgl1 \
    libglib2.0-bin \
    ninja-build \
    pkg-config \
    libffi-dev \
    libmount-dev \
    libselinux1-dev \
    libpcre2-dev \
    libz-dev \
    wget \
    python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install meson
RUN pip install packaging

RUN mkdir -p /tmp/glib-build \
    && cd /tmp/glib-build \
    && apt-get update && apt-get install -y wget \
    && wget https://download.gnome.org/sources/glib/2.80/glib-2.80.3.tar.xz \
    && tar -xvf glib-2.80.3.tar.xz \
    && cd glib-2.80.3 \
    && meson setup build \
    && ninja -C build \
    && ninja -C build install \
    && ldconfig \
    && rm -rf /tmp/glib-build

COPY docker/requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app

COPY src/ ./src/
COPY tests/ ./tests/

RUN pyinstaller --hidden-import=pycountry --hidden-import=babel --hidden-import=requests --hidden-import=geopy --hidden-import=bs4 --hidden-import=groq --hidden-import=PyQt5.sip --add-data="src/commands/*:commands" --add-data="src/utils/*:utils" --add-data="/usr/local/lib/python3.11/site-packages/PyQt5/Qt5/plugins/platforms:platforms" --onefile --name luna_linux src/main.py