FROM ubuntu

ARG file="hello.py"
ENV welcome hello

ADD $file /
ENV fileName=$file

RUN apt-get update && apt-get install -y python

ENTRYPOINT [ "python" ]
CMD [ "hello.py" ]
