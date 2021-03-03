import json
import csv
import boto3
import os

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++ Esta Lambda se gatilla con la SQS  +++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


ddb = boto3.resource('dynamodb')
table = ddb.Table(os.environ['TABLE_NAME'])

def lambda_handler(event, contex):
    sqs_queue_url = os.environ.get('ENV_SQS_QUEUE')
    region_name = os.environ.get('ENV_REGION_NAME')
    print('--Inicia--')
    sqs = boto3.client('sqs', region_name=region_name)

    print('Se han encontrado {} archivo(s) en el bucket nuevo(s)'.format(len(event['Records'])))
    if 'Records' in event:
        for rec in event['Records']:
            print('Procesando {}...'.format(rec['messageId']))
            receipt_handle = rec['receiptHandle']
            body = rec['body']
            ctr = json.loads(body)
            #print ("contenido: ",ctr)
            res = save_item_ddb(table,ctr)
            print ("Respuesta ddb Cliente: ",res)
            

            if ((res["ResponseMetadata"]["HTTPStatusCode"] == 200)):
                sqs.delete_message( QueueUrl=sqs_queue_url, ReceiptHandle=receipt_handle)
                print('Mensaje {} borrado'.format(rec['messageId'])) 


    print('\n---Fin de Ejecución---\n') 
 
    return 0

def save_item_ddb(table,item):
    response = table.put_item(Item=item)
    return response

