#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
from __future__ import print_function
from mimetypes import MimeTypes
import signal, sys, os
import time
import subprocess
import logging
import MySQLdb
import boto3
from boto3.s3.transfer import S3Transfer
from config import *

def insertData(thumbnail, optimized, original):
    db = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASS, db=DB_NAME)
    cur = db.cursor()
    cur.execute('''
      INSERT INTO uploaded_images 
      (thumbnail, optimized, original, datetime)
      VALUES (%s, %s, %s, %s)
      ''', (thumbnail, optimized, original, time.strftime("%Y-%m-%d", time.gmtime())) )
    db.commit()
    db.close()

def getMessagesFromQueue():
    mime = MimeTypes()
    
    # connect to sqs queue
    sqs = boto3.resource('sqs', region_name=AWS_REGION)
    queue = sqs.get_queue_by_name(QueueName=QUEUE_NAME)
    
    while(True):
        # read by one message from queue
        for message in queue.receive_messages(MaxNumberOfMessages=1):
            image_key = message.body
            image_folder = image_key.rsplit("/", 1)[0]
            image_name = image_key.rsplit("/", 1)[1]
            print("[%s] Processing message for %s image..." % (time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()), image_key))
            
            # connect to the s3
            s3 = boto3.client('s3', region_name=AWS_REGION)
            transfer = S3Transfer(s3)
            
            # download, convert and upload image
            file_name = TMP_DIR + image_name
            optimized_file = image_name.rsplit(".", 1)[0] + "_optimized." + image_name.rsplit(".", 1)[1]
            thumbnail_file = image_name.rsplit(".", 1)[0] + "_200x200." + image_name.rsplit(".", 1)[1]
            
            transfer.download_file(BUCKET_NAME, image_key, file_name)
            try:
                subprocess.call(["/usr/bin/convert", file_name, "-quality", "70%", TMP_DIR + optimized_file])
                subprocess.call(["/usr/bin/convert", "-background", "#0008", "-fill", "white", "-gravity", 
                                 "center", "-size", "500x50", "caption:" + WATERMARK, TMP_DIR + optimized_file, 
                                 "+swap", "-gravity", "south", "-composite", TMP_DIR + optimized_file])
                transfer.upload_file(TMP_DIR + optimized_file, BUCKET_NAME, image_folder + "/" + optimized_file, 
                                     extra_args={'ContentType': mime.guess_type(TMP_DIR + optimized_file)[0], 'ACL': 'public-read'})
                os.remove(TMP_DIR + optimized_file)
                
                subprocess.call(["/usr/bin/convert", "-thumbnail", "200x200", file_name, TMP_DIR + thumbnail_file])
                subprocess.call(["/usr/bin/convert", "-background", "#0008", "-fill", "white", "-gravity", 
                                 "center", "-size", "200x30", "caption:" + WATERMARK, TMP_DIR + thumbnail_file, 
                                 "+swap", "-gravity", "south", "-composite", TMP_DIR + thumbnail_file])
                transfer.upload_file(TMP_DIR + thumbnail_file, BUCKET_NAME, image_folder + "/" + thumbnail_file, 
                                     extra_args={'ContentType': mime.guess_type(TMP_DIR + thumbnail_file)[0], 'ACL': 'public-read'})
                os.remove(TMP_DIR + thumbnail_file)
            
            except Exception:
                pass
            
            insertData(image_folder + "/" + thumbnail_file, image_folder + "/" + optimized_file, image_key)
            os.remove(file_name)
            
            # remove processed message from queue
            message.delete()
        
        time.sleep(30)

logging.basicConfig(
    filename=LOG_FILENAME,
    level=logging.INFO,
    format='[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%s',
)
if __name__ == '__main__':
    getMessagesFromQueue()
