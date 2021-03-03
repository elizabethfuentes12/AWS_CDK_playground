from aws_cdk import (
    aws_s3 as s3,
    aws_s3_notifications,
    aws_sqs as sqs,
    aws_lambda,
    aws_dynamodb as ddb,
    aws_lambda_event_sources,

    core
)

class S3ToDynamoStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        REGION_NAME = 'us-east-1'

        #+++++++++++++++++++++++++++++++++++
        #++++++++++Creamos el bucket +++++++
        #+++++++++++++++++++++++++++++++++++

        bucket = s3.Bucket(self,"s3-dynamodb" ,  versioned=False, removal_policy=core.RemovalPolicy.DESTROY)

        #removal_policy=DESTROY, le estamos indicando que cuando eliminemos el stack el bucket tambien se debe borrar, pero esto solo se cumple si el bucket esta vacio. 

        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #++++++++++Creamos SQS: ESta SQS recibirá mensajes de lmabda1 ++++++++++++++++
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


        queue_fail_SQS = sqs.Queue(
            self, "SQS-FAIL-", visibility_timeout=core.Duration.seconds(30))
        dead_letter_SQS = sqs.DeadLetterQueue(
            max_receive_count=10, queue=queue_fail_SQS)
        queue_SQS = sqs.Queue(self, "SQS-INI-", visibility_timeout=core.Duration.seconds(
            30), dead_letter_queue=dead_letter_SQS)


        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #++++++++++Creamos la lmabda1: que se gatilla cuando hay un archivo nuevo en el bucket ++++++++++++++++
        #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        lambda_1 = aws_lambda.Function(self, "lambda-1",
                                    runtime=aws_lambda.Runtime.PYTHON_3_8,
                                    handler="lambda_function.lambda_handler",
                                    timeout=core.Duration.seconds(20),
                                    memory_size=256, description= "Lambda que lee bucket y envia a SQS",
                                    code=aws_lambda.Code.asset("./lambda_1"),
                                    environment={'ENV_SQS_QUEUE': queue_SQS.queue_url,
                                    'ENV_REGION_NAME': REGION_NAME
                                      })

        #Permiso para leer de S3 y se agrega el evento que la activara 

        bucket.grant_read(lambda_1)   
        notification = aws_s3_notifications.LambdaDestination(lambda_1)
        bucket.add_event_notification(s3.EventType.OBJECT_CREATED, notification) 
        queue_SQS.grant_send_messages(lambda_1)


        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #+++++++++++++++++++++++++++++++++++ Creamos la tabla DynamoDB ++++++++++++++++++++++++++++++++++++++++++
        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

        ddb_table = ddb.Table(
            self, "Tabla",
            partition_key=ddb.Attribute(name="campo1", type=ddb.AttributeType.STRING),
            sort_key=ddb.Attribute(name="campo2", type=ddb.AttributeType.STRING),
            removal_policy=core.RemovalPolicy.DESTROY)
        



        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #+++++++++ Creamos la lmabda2: que se gatilla al recibir un SQS y escribe en la DynamoDB ++++++++++++++++
        #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


        lambda_2 = aws_lambda.Function(self, "lambda_2",
                                    runtime=aws_lambda.Runtime.PYTHON_3_8,
                                    handler="lambda_function.lambda_handler",
                                    timeout=core.Duration.seconds(20),
                                    memory_size=256, description= "Lambda lee SQS y escribe en DDB",
                                    code=aws_lambda.Code.asset("./lambda_2"),
                                    environment={'ENV_SQS_QUEUE': queue_SQS.queue_url,
                                          'ENV_REGION_NAME': REGION_NAME
                                      })

        #Permiso para escribir en la tabla
        ddb_table.grant_write_data(lambda_2)   
        lambda_2.add_environment("TABLE_NAME", ddb_table.table_name)
        
        #Permiso para leer de SQS en la tabla
        queue_SQS.grant_consume_messages(lambda_2)

        #EL evento que gatilla la lambda

        event_source = aws_lambda_event_sources.SqsEventSource(
            queue_SQS, batch_size=1)
        lambda_2.add_event_source(event_source) 

        

