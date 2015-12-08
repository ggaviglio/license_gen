FROM python:3.4

#Install ssh key so this project can access private repositories
RUN mkdir -p /root/.ssh
ADD ./keys/wid-internal-container-key /root/.ssh/id_rsa
RUN chmod 600 /root/.ssh/id_rsa
RUN ssh-keyscan gitlab.alfresco.com >> /root/.ssh/known_hosts

#Install Java for the license generators
RUN yum install -y java

WORKDIR /usr/src/app/

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app