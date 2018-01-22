# deliveryh-service

This application aims to expose a suite of endpoints to perform CRUD operations on restaurants.

## prerequisites

- *docker* 
- *docker-compose*

## local set-up

start the dev server for local development: ``docker-compose up``

now the app should be accessible on the local machine on port **:8000**

**note:** if that port is busy on the local machine, change the port to expose to in the ``docker-compose.yml`` file:
under the _web_ service, in the _ports_ section, edit the left side with a port of your choice (for example **"8000:8000"** becomes **"1357:8000"**)

## api specification

interactive documentation can be found on the route ``/docs``