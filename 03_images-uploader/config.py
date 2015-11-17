#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

APP_HOST = str(os.environ.get('APP_HOST', '0.0.0.0'))
APP_PORT = int(os.environ.get('APP_PORT', 8080))

QUEUE_NAME = str(os.environ.get('SQS_QUEUE_NAME', ''))
BUCKET_NAME = str(os.environ.get('S3_BUCKET_NAME', ''))
AWS_REGION = str(os.environ.get('AWS_REGION', 'eu-west-1'))
UPLOAD_DIR = str(os.environ.get('UPLOAD_DIR', '/tmp/'))

IMAGE_TYPES = set(['png', 'jpg', 'jpeg', 'bmp'])

DB_HOST = str(os.environ.get('DB_HOST', ''))
DB_USER = str(os.environ.get('DB_USER', ''))
DB_PASS = str(os.environ.get('DB_PASS', ''))
DB_NAME = str(os.environ.get('DB_NAME', ''))

LOG_FILENAME = str(os.environ.get('LOG_FILENAME', '/var/log/images-uploader.log'))