FROM jupyter/base-notebook
RUN pip install pymongo
RUN pip install kafka-python
COPY ./jupyter/ /home/jovyan/work/
USER root

