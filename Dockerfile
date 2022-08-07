FROM continuumio/miniconda3:latest

RUN conda install pip ffmpeg; pip install pydub pyttsx3 flask
RUN apt-get update
RUN apt-get install -y libespeak-dev

WORKDIR /app/
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]

ADD app.py /app/app.py