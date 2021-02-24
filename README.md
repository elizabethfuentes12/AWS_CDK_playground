# AWS_CDK_playground
Iniciando en AWS CDK
[fuente](https://cdkworkshop.com/30-python/20-create-project/100-cdk-init.html)

### 1. Primero hay que crear las carpetas de nuestro proyecto. 

```
mkdir cdkworkshop && cd cdkworkshop
```

### 2. Iniciando CDK

```
cdk init sample-app --language python
```

Y obtendras la siguiente respuesta: 

```
Applying project template sample-app for python

# Welcome to your CDK Python project!

You should explore the contents of this project. It demonstrates a CDK app with an instance of a stack (`stack_stack`)
which contains an Amazon SQS queue that is subscribed to an Amazon SNS topic.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization process also creates
a virtualenv within this project, stored under the .venv directory.  To create the virtualenv
it assumes that there is a `python3` executable in your path with access to the `venv` package.
If for any reason the automatic creation of the virtualenv fails, you can create the virtualenv
manually once the init process completes.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

You can now begin exploring the source code, contained in the hello directory.
There is also a very trivial test included that can be run like this:

```
$ pytest
```

To add additional dependencies, for example other CDK libraries, just add to
your requirements.txt file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!

Please run 'python3 -m venv .venv'!
Executing Creating virtualenv...
✅ All done!
❯ cd..
zsh: command not found: cd..
❯ cd ..
❯ git status
En la rama main
Tu rama está actualizada con 'origin/main'.

Cambios no rastreados para el commit:
  (usa "git add <archivo>..." para actualizar lo que será confirmado)
  (usa "git restore <archivo>..." para descartar los cambios en el directorio de trabajo)
	modificado:     .gitignore
	modificado:     README.md

Archivos sin seguimiento:
  (usa "git add <archivo>..." para incluirlo a lo que se será confirmado)
	diagrama.jpeg
	stack/

sin cambios agregados al commit (usa "git add" y/o "git commit -a")
❯ git add .
git commit -m “Carga1”
git push
[main 4833c1d] “Carga1”
 15 files changed, 224 insertions(+), 6 deletions(-)
 create mode 100644 diagrama.jpeg
 create mode 100644 stack/.gitignore
 create mode 100644 stack/README.md
 create mode 100644 stack/app.py
 create mode 100644 stack/cdk.json
 create mode 100644 stack/requirements.txt
 create mode 100644 stack/setup.py
 create mode 100644 stack/source.bat
 create mode 100644 stack/stack/__init__.py
 create mode 100644 stack/stack/stack_stack.py
 create mode 100644 stack/tests/__init__.py
 create mode 100644 stack/tests/unit/__init__.py
 create mode 100644 stack/tests/unit/test_stack_stack.py
Enumerando objetos: 22, listo.
Contando objetos: 100% (22/22), listo.
Compresión delta usando hasta 4 hilos
Comprimiendo objetos: 100% (16/16), listo.
Escribiendo objetos: 100% (19/19), 64.13 KiB | 9.16 MiB/s, listo.
Total 19 (delta 1), reusado 0 (delta 0), pack-reusado 0
remote: Resolving deltas: 100% (1/1), completed with 1 local object.
To https://github.com/elizabethfuentes12/Stream_Connet.git
   5c8ec0c..4833c1d  main -> main
❯ cd stack
❯ source .env/bin/activate

source: no such file or directory: .env/bin/activate
❯ ls
README.md        cdk-firehose     cdk.json         setup.py         stack
app.py           cdk-lambda       requirements.txt source.bat       tests
❯ cd stack
❯ ls
__init__.py    stack_stack.py
❯ cd ..
❯ ls
ls: .: Operation not permitted
❯ cd ..
❯ cd..
zsh: command not found: cd..
❯ cd ..
❯ ls
Applications              Downloads                 Music                     Zotero                    miniconda3
Desktop                   Library                   Pictures                  anaconda3                 powerlevel10k
Documents                 Movies                    Public                    bin                       spark-3.0.0-bin-hadoop2.7
❯ cd Documents
❯ cd AWS_cosas
❯ ls
AWS_CDK_playground Certificados       Stream_Connet      cdk-mini-patterns  connect
❯ cd Stream_Connet
❯ cd stack
❯ cdk init sample-app --language python

Applying project template sample-app for python

# Welcome to your CDK Python project!

You should explore the contents of this project. It demonstrates a CDK app with an instance of a stack (`stack_stack`)
which contains an Amazon SQS queue that is subscribed to an Amazon SNS topic.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization process also creates
a virtualenv within this project, stored under the .venv directory.  To create the virtualenv
it assumes that there is a `python3` executable in your path with access to the `venv` package.
If for any reason the automatic creation of the virtualenv fails, you can create the virtualenv
manually once the init process completes.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

You can now begin exploring the source code, contained in the hello directory.
There is also a very trivial test included that can be run like this:

```
$ pytest
```

To add additional dependencies, for example other CDK libraries, just add to
your requirements.txt file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!

Please run 'python3 -m venv .venv'!
Executing Creating virtualenv...
✅ All done!
```

### 3. Istalar los requerimientos para el ambiente de python: 

```
pip install -r requirements.txt
```


