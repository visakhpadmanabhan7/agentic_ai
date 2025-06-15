FROM ubuntu:latest
LABEL authors="visakh"

ENTRYPOINT ["top", "-b"]