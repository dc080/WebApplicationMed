FROM python

RUN apt update && apt install ffmpeg libsm6 libxext6 -y 
RUN pip install flask flask_sqlalchemy opencv-python fire pylab-sdk requests pillow matplotlib flask-session
