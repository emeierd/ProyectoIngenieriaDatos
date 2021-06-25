FROM puckel/docker-airflow:latest

ENV PYTHONPATH "${PYTHONPATH}:/src:/usr/local/airflow/dags"

USER root
ENV TZ=Chile
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update
RUN apt-get install python3-dev -y


RUN pip3 install requests
RUN pip3 install pandas
RUN pip3 install pymongo
RUN pip3 install kafka-python
ENV SHARE_DIR /usr/local/share

RUN touch /var/run/docker.sock
RUN chown -R airflow /var/run/docker.sock
