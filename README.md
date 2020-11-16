# DS4A-final-project-team-64
This repository contain the sources file of the project developed by the team 64in the course DS4A.


**Aplication Folder:**

In this folder are all the source files necessary to deploy the application in a local environment. The application runs with the flask python library. then the files that the folder contains.

* app.py: It is the main file, it is executed with python app.py
* encoderCats.p: This file contains the encoder created in the model training and is used in the prediction
* modelLog.model This file contains the trained model
* scalerEdad.p This file contains the encoder created in the training of the model and is used in the prediction
* Static folder: contains the css, javascript and images files used in the application

**Python files Folder:**

En este folder se encuentran los siguientes archivos:

* loaderSQLPython.iptnb: is used to load the excel files to postgresql database
* mlModelPython: este archivo realiza la prediccion de enfermos en la base de datos de postgres e inserta los resultados en la base de datos
* modelLog.model This file contains the trained model
* scalerEdad.p This file contains the encoder created in the training of the model and is used in the prediction
* Static folder: contains the css, javascript and images files used in the application
* pipeline-Train.ipynb: This notebook contain the cleaning, encoding and training of some models.

**application deployed in amazon web services**
http://18.224.184.100:5000/version2






