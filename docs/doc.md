# Italian-Github-Statistics

*Italian-Github-Statistics* is a dashboard that shows statistics of the italian's PA
github repositories. The application is composed of two docker containers which expose both [APIs](./api.doc.md) and [Web Application](./app.doc.md).

## Docker-Compose

```
services:
  api:
    build: ./api
    ...
  client-js:
    build: ./public
```

