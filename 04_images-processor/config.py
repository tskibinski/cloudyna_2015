#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

QUEUE_NAME = str(os.environ.get('SQS_QUEUE_NAME', ''))
BUCKET_NAME = str(os.environ.get('S3_BUCKET_NAME', ''))
AWS_REGION = str(os.environ.get('AWS_REGION', 'eu-west-1'))
TMP_DIR = str(os.environ.get('TMP_DIR', '/tmp/'))
WATERMARK = str(os.environ.get('WATERMARK', 'default-watermark'))

DB_HOST = str(os.environ.get('DB_HOST', ''))
DB_USER = str(os.environ.get('DB_USER', ''))
DB_PASS = str(os.environ.get('DB_PASS', ''))
DB_NAME = str(os.environ.get('DB_NAME', ''))

LOG_FILENAME = str(os.environ.get('LOG_FILENAME', '/var/log/images-processor.log'))