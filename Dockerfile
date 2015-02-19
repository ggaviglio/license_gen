FROM centos6-python3-django

WORKDIR /opt/django_project

COPY . /opt/django_project
RUN pip3.4 install -r requirements.txt

#Allow external from a requirements file didn't seem to work
RUN pip3.4 install mysql-connector-python --allow-external mysql-connector-python

EXPOSE 80

CMD ["supervisord", "-n"]