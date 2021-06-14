# CSV to DynamoDB Loader

## Un cargador de archivos CSV a DynamodB en menos de 5 minutos con Cloud Develepment Kit (CDK).

Últimamente he estado desarrollado algunas aplicaciones que han requerido alimentar una base de datos DynamoDB desde archivos CSV. Por esto se me ocurrió generar una pequeña aplicación serverless utilizando CDK lista para estas situaciones. Les comparto esta aplicación para sus proyectos.

En este tutorial vamos a ver como crear una aplicación sencilla en CDK con Python, pero extremadamente útil. Como se ve en la siguiente imagen, cada vez que se sube un archivo al bucket, un evento invoca una función Lambda (Lambda1) que se encarga de leer el archivo .CSV del bucket, envía cada línea como un mensaje a una cola SQS. Esta cola tiene otro desencadenador que invoca otra función Lambda (Lambda2) que toma el mensaje y los escribe como un ítem de una tabla DynamoDB.

!["Diagrama"](imagen/playground_1.jpg)

Los servicios involucrados en esta solución son:

### Amazon S3 (Simple Storage Service):
[S3](https://aws.amazon.com/es/s3/) es un servicio de computo sin servidor que le permite ejecutar código sin aprovisionar ni administrar servidores.

### AWS Lamdba: 
AWS [Lambda](https://aws.amazon.com/es/lambda/) es un servicio de computo sin servidor que le permite ejecutar código sin aprovisionar ni administrar servidores, 

### Amazon SQS (Simple Queue Service):
[SQS](https://aws.amazon.com/es/sqs/) Es un servicio de colas de mensajes completamente administrado que permite desacoplar y ajustar la escala de microservicios, sistemas distribuidos y aplicaciones serverless.
 
### Amazon DynamoDB:
Amazon [DynamoDB](https://docs.aws.amazon.com/es_es/amazondynamodb/latest/developerguide/Introduction.html) es un servicio de base de datos de NoSQL completamente administrado que ofrece un desempeño rápido y predecible, así como una escalabilidad óptima. DynamoDB le permite reducir las cargas administrativas que supone tener que utilizar y escalar una base de datos distribuida, lo que le evita tener que preocuparse por el aprovisionamiento del hardware, la configuración y la configuración, la replicación, los parches de software o el escalado de clústeres.


### CDK (Cloud Development Kit): 
El kit de desarrollo de la nube de AWS (AWS CDK) es un framework de código abierto que sirve para definir los recursos destinados a aplicaciones en la nube mediante lenguajes de programación conocidos.

Una vez lo conozcas... no vas a querer desarrollar aplicaciones en AWS de otra forma ;)

Conoce más acá: [CDK](https://aws.amazon.com/es/cdk/?nc1=h_ls)


## Despliegue

**Para crear la aplicación debes seguir los siguientes pasos:**

### 1. Instalar CDK

Para realizar el despliegue de los recursos, debes instalar y configurar la cli (command line interface) de CDK, en este caso estamos utilizando CDK con Python.

[Instalación y configuración de CDK](https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html)

[Documentación CDK para Python](https://docs.aws.amazon.com/cdk/api/latest/python/index.html)


### 2. Clonamos el repo y vamos la carpeta de nuestro proyecto. 

```bash
git clone https://github.com/elizabethfuentes12/AWS_CDK_playground
cd AWS_CDK_playground/s3_to_dynamo
```

### 3. Creamos e iniciamos el ambiente virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Este ambiente virtual (venv) nos permite aislar las versiones del python que vamos a utilizar como también de librerías asociadas. Con esto podemos tener varios proyectos con distintas configuraciones.
___
## 4. Explicación del codigo
En el GitHub esta el código listo para desplegar, a continuación una breve explicación:

El .py "orquestador" de nuestra aplicación con el nombre compuesto de la carpeta y la palabra ***_stack*** al final [s3_to_dynamo_stack.py](https://github.com/elizabethfuentes12/AWS_CDK_playground/tree/main/s3_to_dynamo/s3_to_dynamo/s3_to_dynamo_stack.py) 


En este archivo se definen los recursos a desplegar por ejemplo el bucket s3:

### Bucket

API Reference para [aws_cdk.aws_s3](https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_s3.html)

Debemos agregar el uso de la libreria de aws_s3

```python
import aws_s3 as s3

bucket = s3.Bucket(self,"s3-dynamodb",
        versioned=False, removal_policy=core.RemovalPolicy.DESTROY)
```

Comando para crear el Bucket con sus respectivas politicas (opcional), en este caso usaremos removal_policy = DESTROY para que el bucket se elimine cuando eliminemos el stack. 

Revisa mas de esta API en [Bucket](https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_s3/Bucket.html)


### Crear SQS que recibirá los mensajes de Lambda1: 

API Reference para [aws_cdk.aws_sqs](https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_sqs.html)


```python
import aws_sqs as sqs

#Primero creamos la Queue de mensajes fallidos, ya que las otras dos le hacen mención.

queue_fail_SQS = sqs.Queue(self, "SQS-FAIL-", visibility_timeout=core.Duration.seconds(30))

#A continuación creamos la Queue DeadLetterQueue, para donde se iran todos los mensajes fallidos de la Queue principal o "cola"

dead_letter_SQS = sqs.DeadLetterQueue(max_receive_count=10, queue=queue_fail_SQS)

#Por último, creamos la Queue (o cola), la nombramos "SQS-INI" visibility_timeout de 30 segundos y le indicamos que los mensajes sin procesar deben irse a la dead_letter_queue creada anteriormente.

queue_SQS = sqs.Queue(self, "SQS-INI-", visibility_timeout=core.Duration.seconds(30), dead_letter_queue=dead_letter_SQS)

```

Para un mejor manejo de los mensaje, utilizaremos una cola principal y una cola que almacene los mensajes fallidos. 

API SQS [Queue](https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_sqs/Queue.html)


API [DeadLetterQueue](https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_sqs/DeadLetterQueue.html)



Luego de esto creamos la una función lambda que es gatillada al cargar un archivo nuevo en el bucket y envía las linea que lee a una cola SQS:


### Función Lambda1: 

API [aws_lambda](https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_lambda.html)


```python 
import aws_lambda

lambda_1 = aws_lambda.Function(
    self, "lambda-1",
    runtime=aws_lambda.Runtime.PYTHON_3_8,
    handler="lambda_function.lambda_handler",
    timeout=core.Duration.seconds(20),
    memory_size=256, description= "Lambda que lee bucket y envia a SQS",code=aws_lambda.Code.asset("./lambda_1"),
    environment={'ENV_SQS_QUEUE': queue_SQS.queue_url,
    'ENV_REGION_NAME': REGION_NAME})

```
Creamos la Lambda con el siguiente comando
API [Function](https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_lambda/Function.html)

Estas lambdas se gatillan con eventos, por lo cual debemos agregar la librería que lo permite. 

API [aws_lambda_event_sources](https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_lambda_event_sources.html)


Los parámetros son los estándares que generalmente configuramos cuando creamos una función Lambda por CLI o por la consola, y además le agregamos las variables de entorno necesarias en el código de la lambda: 

| Nombre | Valor | Descripcion |
|---|---|---|
| ENV_SQS_QUEUE | queue_SQS.queue_url | Es la URL de la Queue |
| ENV_REGION_NAME | Nombre de la region | Opcional si se requiere para defenir la Queue dentro de Lambda1 |


El código python que ejecuta esta lambda se encuentra en la carpeta [/lambda_1](https://github.com/elizabethfuentes12/AWS_CDK_playground/tree/main/s3_to_dynamo/lambda_1)



### Trigger de nuevo objeto en el bucket. 

```python
import aws_s3_notifications

#Para que se gatille al cargar un nuevo archivo en S3, debemos crear la notificación

notification = aws_s3_notifications.LambdaDestination(lambda_1)

#Agregamos el evento a la Lambda e indicamos que este se debe gatillar cuando se crea un archivo en S3. 
bucket.add_event_notification(s3.EventType.OBJECT_CREATED, notification)

#Y por supuesto le damos permiso a la Lambda1 para que pueda leer del bucket S3. 
bucket.grant_read(lambda_1)

#Para que la lambda pueda escribir en la SQS definida se le debe dar permiso
queue_SQS.grant_send_messages(lambda_1)
```

API [aws_cdk.aws_s3_notifications](https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_s3_notifications/LambdaDestination.html)


### Tabla DynamoDB


API [aws_dynamodb](https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_dynamodb.html)

Le agregamos los parámetros al igual que por CLI o por la consola, y para nuestro ejemplo definimos las key.


| Tipo de Key| Key name | Type |
|---|---| ---|
| partition key | campo1 | string |
| sort key | campo2 | string |


```python 
import aws_dynamodb as ddb
ddb_table = ddb.Table(
    self, "Tabla",
    partition_key=ddb.Attribute(name="campo1", type=ddb.AttributeType.STRING),
    sort_key=ddb.Attribute(name="campo2", type=ddb.AttributeType.STRING),
    #Y  definimos RemovalPolicy como DESTROY para que se borre cuando se elimina el Stack de la aplicación. 
    removal_policy=core.RemovalPolicy.DESTROY)
```

API [Table](https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_dynamodb/Table.html)






### Funcion Lambda2: 

Creamos la lambda que se gatilla con la SQS y escribe en Tabla:


```python
lambda_2 = aws_lambda.Function(
    self, "lambda_2",runtime=aws_lambda.Runtime.PYTHON_3_8,handler="lambda_function.lambda_handler",
    timeout=core.Duration.seconds(20),
    memory_size=256, description= "Lambda lee SQS y escribe en DDB",
    code=aws_lambda.Code.asset("./lambda_2"),
    environment={'ENV_SQS_QUEUE': queue_SQS.queue_url,
    'ENV_REGION_NAME': REGION_NAME})

#Se le otorgan permisos para que pueda escribir en la tabla DynamoDB
ddb_table.grant_write_data(lambda_2)

# tambien podemos agregar la variable de entorno para la DynamoDB con un comando aparte. 
lambda_2.add_environment("TABLE_NAME", ddb_table.table_name)
```

La definimos igual que la anterior con la diferencia del nombre, la descripción y de la carpeta donde tomara la función.




Lambda2 se gatilla con la recepción de mensajes desde la cola SQS, debemos crear y agregar el evento a la Lambda2:

```python 
import aws_lambda_event_sources

event_source = aws_lambda_event_sources.SqsEventSource(queue_SQS, batch_size=1)
lambda_2.add_event_source(event_source) 

queue_SQS.grant_consume_messages(lambda_2)
```
Y le damos permiso para que pueda consumir los mensajes desde la cola, este comando también permite borrar mensajes, lo cual es importante para que una vez sea exitosa la función esta sea capaz de borrar el mensaje de la cola y no sea reintentado.

!["paso_3"](imagen/paso_3.png)

Revisa más en [Queue](https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.aws_sqs/Queue.html)



El código de esta lambda se encuentra en la carpeta [/lambda_2](https://github.com/elizabethfuentes12/AWS_CDK_playground/tree/main/s3_to_dynamo/lambda_2)

___

## ¡¡Felicidades!! ya estamos casi listos para desplegar nuestra aplicación

### 5. Instalamos los requerimientos para el ambiente de python 

Para que el ambiente pueda desplegarse, debemos agregar todas las librerías CDK necesarias en el archivo  [requirements.txt](https://github.com/elizabethfuentes12/AWS_CDK_playground/tree/main/s3_to_dynamo/requirements.txt)


```zsh
pip install -r requirements.txt
```

### 6. Desplegando la aplicación

Previo al despliegue de la aplicación en AWS Cloud debemos asegurarnos que este sin errores para que no salten errores durante el despliegue, eso lo hacemos con el siguiente comando que genera un template de cloudformation con nuestra definición de recuersos en python.

```bash
cdk synth
```

Si hay algún error en tu código este comando te indicara cual es con su ubicación.  

En el caso de estar cargando una nueva version de la apliación puedes revisar que es lo nuevo con el siguiente comando: 

```
cdk diff
```

Procedemos a desplegar la aplicación: 

```
cdk deploy
```

Para ver el estado del despliegue en el terminal: 

!["paso_5"](imagen/paso_5.png)

ó en la consola: 

!["paso_5"](imagen/paso_5_2.png)

Una vez finalizado el despligue puedes ver los recursos creados: 

!["paso_5"](imagen/paso_5_3.png)


### 7. Prueba

Para probar la aplicación busca el bucket en los recursos y agrega el archivo [ejemplo.csv](https://github.com/elizabethfuentes12/AWS_CDK_playground/blob/main/ejemplo.csv)

Y en solo unos segundos puedes ver que tenemos el contenido del csv en la Tabla de DynamoDB

!["paso_6"](imagen/paso_6.png)


Ya que usamos una cola de mensajes no nos preocupa la cantidad de elementos. Todos se insertan eventualmente en la Tabla dynamoDB. Hay que notar que al ser una cola SQS normal, el orden no está asegurado (si se requiere procesar los mensajes en orden consideremos una cola SQS FIFO)

### 8. Tips


Puedes ver en cual región se va a desplegar tu stack en el archivo [app.py](https://github.com/elizabethfuentes12/AWS_CDK_playground/blob/main/s3_to_dynamo/app.py) entonces puedes desplegar en otras regiones. 

c
!["paso_7"](imagen/paso_7.png)


El despliegue lo utiliza utlizando las credenciales por defecto de AWS, si desea usar un profile específico agrege --profile <nombre> al comando deploy:

```
cdk deploy --profile mi-profile-custom
```

o simplemente exporte en una variable de entorno

```
export AWS_PROFILE=mi-profile-custom
cdk deploy
```

En el archivo [comandos.md](https://github.com/elizabethfuentes12/AWS_CDK_playground/blob/main/comandos.md) esta el resumen de los comandos CDK utilizados. 



### 9. Eliminar el stack de la aplicación

Para eliminar el stack lo puedes hacer via comando:

```
cdk destroy
```

ó via consola cloudformation, seleccione el stack (mismo nombre del proyecto cdk) y lo borra.

### 10. Adicional

Puedes modificar la DynamoDB para que cada vez que un Items sea cargado lo envié a una Lambda u otro servicio AWS a través de Dynamo Streams [Documentación](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_streams_StreamRecord.html).

En este GitHub puedes ver como hacerlo --> [https://github.com/cdk-patterns/serverless/tree/main/the-dynamo-streamer/python](https://github.com/cdk-patterns/serverless/tree/main/the-dynamo-streamer/python)

## ¡¡Happy developing 😁!!

