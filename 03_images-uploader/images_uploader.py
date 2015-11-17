#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from __future__ import print_function
from flask import Flask
from flask import request, redirect, url_for, render_template, send_from_directory, session
from flask.ext.mysql import MySQL
from werkzeug import secure_filename
from mimetypes import MimeTypes
import os
import time
import logging
import boto3
from boto3.s3.transfer import S3Transfer
from config import *

image_uploader = Flask(__name__)
mysql = MySQL()
image_uploader.config['MYSQL_DATABASE_USER'] = DB_USER
image_uploader.config['MYSQL_DATABASE_PASSWORD'] = DB_PASS
image_uploader.config['MYSQL_DATABASE_DB'] = DB_NAME
image_uploader.config['MYSQL_DATABASE_HOST'] = DB_HOST
mysql.init_app(image_uploader)

#
# Help functions
#
def allowed(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in IMAGE_TYPES

def put_s3_objetct(image_name, storage_dir):
    mime = MimeTypes()
    s3 = boto3.client('s3', region_name=AWS_REGION)
    transfer = S3Transfer(s3)
    image_path = os.path.join(UPLOAD_DIR, image_name)
    key_name = storage_dir + "/" + image_name
    transfer.upload_file(image_path, BUCKET_NAME, key_name, extra_args={'ContentType': mime.guess_type(image_path)[0]})

def send_sqs_msg(image_name, storage_dir):
    message_body = storage_dir + "/" + image_name
    sqs = boto3.resource('sqs', region_name=AWS_REGION)
    queue = sqs.get_queue_by_name(QueueName=QUEUE_NAME)
    response = queue.send_message(MessageBody=message_body)

#
# App routes
#
@image_uploader.route('/upload', methods=['GET', 'POST'])
def upload():
    uploaded = False
    filename = None
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed(file.filename.lower()):
            uploaded = True
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_DIR, filename))
            
            storage_dir = time.strftime("%Y/%m/%d")
            put_s3_objetct(filename, storage_dir)
            send_sqs_msg(filename, storage_dir)
            
            os.remove(os.path.join(UPLOAD_DIR, filename))
            
            return render_template('upload.html', uploaded=uploaded, filename=filename)
    
    return render_template('upload.html', uploaded=uploaded, filename=filename)

@image_uploader.route('/list_images', methods=['GET'])
def list_images():
    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM uploaded_images")
    rows = cur.fetchall()
    conn.close()
    return render_template('list.html', rows=rows, region_name=AWS_REGION, bucket_name=BUCKET_NAME)

@image_uploader.route('/')
def main():
    return render_template('index.html')

logging.basicConfig(
    filename=LOG_FILENAME,
    level=logging.INFO,
    format='[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%s',
)
if __name__ == '__main__':
    host = APP_HOST
    port = APP_PORT
    
    image_uploader.debug = True
    
    image_uploader.run(
        host=host,
        port=port,
        threaded=True
    )
