# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.11.9-bookworm

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0
RUN apt-get install -y busybox
RUN apt-get install -y libgtk2.0-dev pkg-config
RUN apt-get install -y qtbase5-dev
RUN apt-get install -y qt5-qmake
RUN apt-get install -y cmake 
RUN apt-get install -y libxkbcommon-x11-0

RUN apt-get install -y build-essential
RUN apt-get install -y python3-dev
RUN apt-get install -y git
RUN apt-get install -y libboost-python-dev
RUN apt-get install -y libboost-system-dev
RUN apt-get install -y libopenblas-dev
RUN apt-get install -y liblapack-dev
RUN apt-get install -y libx11-dev
RUN apt-get install -y libgtk-3-dev
RUN apt-get install -y libavcodec-dev
RUN apt-get install -y libavformat-dev
RUN apt-get install -y libswscale-dev

# Install pip requirements
COPY requirements.txt .
RUN pip install --upgrade pip && python -m pip install -r requirements.txt

RUN git clone https://github.com/davisking/dlib /tmp/dlib \
    && mkdir /tmp/dlib/build \
    && cd /tmp/dlib/build \
    && cmake .. \
    && cmake --build . --config Release \
    && cd /tmp/dlib \
    && python3 setup.py install \
    && rm -rf /tmp/dlib

WORKDIR /app
COPY . /app

# Xserver
ENV DISPLAY host.docker.internal:0.0

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
#RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
#USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
#CMD ["python", "main.py"]
