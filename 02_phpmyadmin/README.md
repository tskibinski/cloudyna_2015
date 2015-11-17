# phpMyAdmin container Service


Resources to build customized Docker image with pre-configured nginx and phpMyAdmin.


### Build

Build new image with below command:

```
docker build --rm -t pma:latest -f Dockerfile .
```


### Usage

Run container in background (as daemon):

```
docker run -d --name pma -p 8080:80 \
  -e DB_HOST=database-endpoint.eu-west-1.rds.amazonaws.com \
  pma:latest
```

Run container in interactive mode with bash shell as entrypoint:

```
docker run -it --rm -p 8080:80 --entrypoint=/bin/bash \
  -e DB_HOST=database-endpoint.eu-west-1.rds.amazonaws.com \
  pma:latest
```

#### Variables

``DB_HOST`` variable is mandatory and specifies the database server address.


### Clean up

Stop and next running container

```
docker stop pma && docker rm pma
```
