
==============
Prerequisites:
==============

Docker:
It requires docker installed on host machine. Kindly find the steps to install docker on Ubuntu in below mentioned link.

https://docs.docker.com/install/linux/docker-ce/ubuntu/

For different OS, steps are available on the same portal.

Commands in this document are for Ubuntu, as my docker host machine is Ubunutu. Please apply similar commands for your OS.


=============================
Part 1 - FreeswitchDockerfile
=============================

Steps to setup:

git clone https://github.com/mitesht/fs-rest-api.git

cd fs-rest-api/

cp FreeswitchDockerfile Dockerfile

sudo docker build -t fs:1.0 .

sudo docker run --name fs_1.0 --network host -v vol_fs:/var/log/freeswitch -p5060:5060/udp -p5080:5080/udp -p16384-16494:16384-16494/udp -p5060:5060/tcp -p5080:5080/tcp fs:1.0

I have taken container name fs_1.0. You can take of your choice.

You're done for the first part.
You will have two users as mentioned in the document.

As we have used --network=host, you can access the FreeSWITCH service with IP/hostname of the docker host machine.


====================================
Part 2 - FreeswitchRESTAPIDockerfile
====================================

Go to directory fs-rest-api/

cp FreeswitchRESTAPIDockerfile Dockerfile

sudo docker build -t fs_rest_api:1.0 .

sudo docker run --name fs_rest_api_1.0 --network host -v vol_fs:/var/log/freeswitch -p5060:5060/udp -p5080:5080/udp -p16384-16494:16384-16494/udp -p5060:5060/tcp -p5080:5080/tcp -p80:80/tcp fs_rest_api:1.0

You're done. You will have the RESTful api running on port 80. As we have used --network=host, you can access the service with IP/host of the docker host machine.


====================
Example of API calls
====================

1) Outbound call:

URL: http://<host/IP>/api/call
Header: "Content-Type": "application/json"
Method: POST

JSON Input: {"destination": "testplivo1"}
JSON Output: {"message": "ok"}
HTTP response code: 201


2) List calls:

URL: http://<host/IP>/api/call_list
Method: GET

Input: No input required
JSON Output: ["941b2a6f-37f6-43b3-a4d3-a3ef5ffcf229"]
HTTP response code: 200

3) Hangup Call:

URL: http://<host/IP>/api/hangup
Header: "Content-Type": "application/json"
Method: POST

JSON Input: {"uuid": "941b2a6f-37f6-43b3-a4d3-a3ef5ffcf229"}
JSON Output: {"message": "ok"}
HTTP response code: 202

Please note that I have not taken care of security related configuration of FreeSWITCH and of REST API. Meaning, Docker image and container created above are not secure.
