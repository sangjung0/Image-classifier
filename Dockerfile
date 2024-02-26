# For more information, please refer to https://aka.ms/vscode-docker-python
FROM tensorflow/tensorflow:2.15.0.post1-gpu

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0
RUN apt-get install -y busybox
RUN apt-get install -y libgtk2.0-dev pkg-config
RUN apt-get install -y python3-tk

# Install pip requirements
COPY requirements.txt .
RUN pip install --upgrade pip && python -m pip install -r requirements.txt

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