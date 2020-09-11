
# -*- coding: utf-8 -*-
"""
.. module: Serverless S3 Event Processor
    :platform: AWS    
.. moduleauthor:: Bruce Goldfeder
.. contactauthor:: bruce.goldfeder@asetpartners.com zarro_boogs
"""

import os
import json
import boto3
import botocore
import psycopg2
import logging
import sys

# Initialize Logger
logger = logging.getLogger()
# logger.setLevel(logging.INFO)
logger.setLevel(logging.DEBUG)

# Database configuration filename in S3 bucket
g_conf_name = "db_config.json"

s3 = boto3.client('s3')

def lambda_handler(event, context):
    
    resp = {'status': False, 'TotalItems': {} , 'Items': [] }
    
    
    if 'Records' not in event:
        resp = {'status': False, "error_message" : 'No Records found in Event' }
        return resp
    
    for r in event.get('Records'):
        # Lets skip the records that are Put/Object Create events
        #if not ( ( r.get('eventName') == "ObjectCreated:Put" )  and ( 's3' in r ) ) : continue
        d = {}
        d['time']           = r['eventTime']
        d['object_owner']   = r['userIdentity']['principalId']
        d['bucket_name']    = r['s3']['bucket']['name']
        d['key']            = r['s3']['object']['key']
        # Read in the database configuration in file could be encrypted in s3
        # Need to put in the code to read from the s3 bucket later 
        if d['key'] == g_conf_name:
            obj = s3.get_object(Bucket=d['bucket_name'], Key=d['key'])
            #file_content = obj["Body"].read().decode('utf-8')
            #json_conf = obj['Body'].read().decode('utf-8')
            

            json_conf = obj['Body'].read().decode('utf-8','ignore')
            logger.info(json_conf)
            #logger.info("json_conf type ",type(json_conf))

            db_dict = json.loads(json_conf)
            #logger.info("db_dict type ",type(db_dict))
            # Log output from db_config.json file in S3 bucket
            logger.info(json_conf)
            for key, value in db_dict.items():
                foo = ""+key+ '->'+ value
                logger.info(foo)
        resp['Items'].append(d)

    if resp.get('Items'):
        resp['status'] = True
        resp['TotalItems'] = { 'Received': len( event.get('Records') ) , 'Processed': len( resp.get('Items') ) }
    
    logger.info(f"resp:{resp}")

    return resp


if __name__ == '__main__':
    lambda_handler(None, None)
