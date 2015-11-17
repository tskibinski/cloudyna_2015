# Cloudyna 2015

Resources for Workshop: **Create microservice environment on Amazon EC2 Container Service**

## CloudFormation templates

* base-for-ecs-cluster.json - simple base template which creates VPC with public and private subnets and launches RDS instance inside private subnet.

* ecs-cluster.json - full base template which:
  * creates VPC with public and private subnets,
  * launches RDS instance inside private subnet,
  * creates Auto-Scaling group for instances that will be attached to created ECS cluster,
  * creates SQS Queue and S3 bucket for image processing tasks.
* images-processor-service.json - creates ECS task definition and service for ImagesProcessor container.
* images-uploader-service.json - creates ECS task definition and service for ImagesUploader container behind ELB.
* phpmyadmin-service.json - creates ECS task definition and service for phpMyAdmin container begind ELB.

#### Database schema

```
DROP TABLE IF EXISTS `uploaded_images`;
CREATE TABLE `uploaded_images` (
    `image_id` INT(11) NOT NULL AUTO_INCREMENT,
    `thumbnail` VARCHAR(256),
    `optimized` VARCHAR(256),
    `original` VARCHAR(256) NOT NULL,
    `size` VARCHAR(32),
    `datetime` DATE DEFAULT NULL,
    CONSTRAINT `uploaded_images_pk` PRIMARY KEY (`image_id`)
) ENGINE=InnoDB DEFAULT CHARSET=`utf8` COLLATE=`utf8_general_ci`;
```