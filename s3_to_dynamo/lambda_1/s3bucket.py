
import boto3
s3client = boto3.client('s3')

def descarga_archivo(bucket, key, base_path, filename):
    with open(base_path+filename, "wb") as data:
        s3client.download_fileobj(bucket, key, data)
    return True

def sube_archivo(path, filename, bucket, key):
    with open(path+filename, 'rb') as data:
        s3client.upload_fileobj(data,bucket, key)
    return True

def borra_archivo(bucket, key):
    s3client.delete_object(Bucket=bucket, Key=key)
    return True