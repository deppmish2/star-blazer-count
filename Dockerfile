FROM python:3.8-alpine

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

RUN echo "@community http://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories \
&& apk add py3-pandas@community
ENV PYTHONPATH="/usr/lib/python3.8/site-packages"

RUN pip install -r requirements.txt

EXPOSE 9300
CMD ["python", "handle.py"]