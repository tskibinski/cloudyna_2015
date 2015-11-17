# ImagesProcessor container Service


Resources to build Docker image with a very light and simple Python application which optimizes and creates thumbnails for images sent by users.


### Build

Build new image with below command:

```
docker build --rm -t ip:latest -f Dockerfile .
```


### Usage

Run container in background (as daemon):

```
docker run -d --name processor \
  -e SQS_QUEUE_NAME=images-queue \
  -e S3_BUCKET_NAME=configuration-bucket \
  -e WATERMARK=custom-watermak \
  -e DB_HOST=database-endpoint.eu-west-1.rds.amazonaws.com \
  -e DB_USER=admin \
  -e DB_PASS=strongPassword \
  -e DB_NAME=database \
  ip:latest
```

#### Variables

``AWS_REGION`` variable specifies the AWS region in which container is launched (default value: eu-west-1).
 
``SQS_QUEUE_NAME`` queue name to which information about uploaded images will be added.

``S3_BUCKET_NAME`` bucket name where uploaded images will be stored.


``DB_HOST`` specifies the database server address.

``DB_NAME`` specifies the database name in which information about images will be stored.

``DB_USER`` specifies the user name with access to database.

``DB_PASS`` specifies the user password.


``WATERMARK`` specifies customized watermark for thumbnails and optimized images (default value: default-watermark).

### Clean up

Stop and next running container

```
docker stop processor && docker rm processor
```
