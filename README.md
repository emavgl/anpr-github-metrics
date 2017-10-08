# __Italian-GitHub-Statistics__
##Analytics service and frontend for GitHub Issues

*Italian-GitHub-Statistics* is a dashboard that shows statistics of the italian's PA
github repositories. The application is composed of two docker containers which expose both [APIs](./api.doc.md) and [Web Application](./app.doc.md).

### The task
The purpose of this project is to create an analytics platform for GitHub issues.
It has been developed during the __hack.developers.2017__ hackaton.

The task that we tried to accomplish is explained better here: https://github.com/italia/anpr/issues/314 .
We applied our method to extract and plot some statistics from __developers.italia__'s GitHub repositories.

### Technologies
- Docker 
- Python
- GitHub API + PyGithub
- Chart.js
- Angular 1
- Primer CSS

### Architecture
We wrote the back-end using plain Python + __GitHub APIs__.
The front-end has been developed using __Angular 1__ and Google's __Primer CSS__.
For the graph plotting we used __Chart.js__.

### Docker-Compose

```
services:
  api:
    build: ./api
    ...
  client-js:
    build: ./public
```

### Requirements
- Python 3
- requests
- Flask
- gunicorn
- PyGithub
- python-dateutil
- numpy

### Running
See _docs/api.doc.md_ to better understand how to run the project.

### Testing
The code includes a testing file, which exploits Python's __unittest__ library to test the back-end code.
To run it, cd into _api/modules/test_ and run test.py