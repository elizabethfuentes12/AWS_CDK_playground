import json
import csv
import boto3
import os
import s3bucket

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++ Esta lambda se gatilla con el S3 de Cliente y envia a la cola WRITE ++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

BASE_PATH = '/tmp/'
CSV_SEPARATOR = ';'

def lambda_handler(event, contex):
    print('Se han encontrado {} archivo(s) en el bucket nuevo(s)'.format(len(event['Records'])))
    sqs_queue_url = os.environ.get('ENV_SQS_QUEUE')
    
    region_name = os.environ.get('ENV_REGION_NAME')
    sqs = boto3.client('sqs', region_name=region_name)
 
    for record in event['Records']:
        bucket1 = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        filename = key.split('/')[-1]
        s3bucket.descarga_archivo(bucket1, key, BASE_PATH, filename)
        csvFilePath = BASE_PATH+filename
        print('Empieza la lectura de {}'.format(csvFilePath)) 
        
 
        with open(csvFilePath, encoding='utf-8') as csvf:
            csvReader = csv.DictReader(csvf,delimiter=CSV_SEPARATOR)

            for rows in csvReader:
                # Assuming a column named 'CampainID' to
                # be the primary key
                elem = json.loads(json.dumps(rows))
                print ('** enviando', elem, 'mensajes a la cola', sqs_queue_url)
                response = sqs.send_message(
                    QueueUrl=sqs_queue_url,
                    MessageBody=json.dumps(elem))
                
                print ("Respuesta SQS Cliente: ",response)
                
                
    print('\n---Fin de Ejecución---\n')
  
    return 0
