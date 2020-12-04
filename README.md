# DS4A-final-project-team-64
This repository contain the source files of the project developed by the team 64in the course DS4A.


**Aplication Folder:**

In this folder are all the source files necessary to deploy the application in a local environment. The application runs with the flask python library. then the files that the folder contains are:

* app.py: It is the main file, Render the web application and expose the death risk model as an API. It is executed with python app.py
* encoderCats.p: This file contains the encoder created in the model training and is used in the prediction
* modelLog.model This file contains the trained model
* scalerEdad.p This file contains the encoder created in the training of the model and is used in the prediction
* Static folder: contains the css files, javascript files and images files used in the application.

**Python files Folder:**

En este folder se encuentran los siguientes archivos:

* loaderSQLPython.iptnb: Is used to load the excel files provided by the Bucaramanga office to postgresql database
* mlModelPython: This file makes the prediction of the risk of the infected people who do not have a breakdown. The script reads the data from postgresql, performs cleaning, coding, prediction and finally persists the information in postgresql
* modelLog.model This file contains the trained model
* scalerEdad.p This file contains the encoder created in the training of the model and is used in the prediction
* Static folder: contains the css, javascript and images files used in the application
* pipeline-Train.ipynb: This notebook contain the cleaning, encoding and training of some models.

**application deployed in amazon web services**
http://3.134.105.195:5000/version2

**Architecture_diagram.jpeg**
* It is the image of the architecture diagram used for the construction of the application.

![alt text](https://github.com/yeissonzamora/DS4A-final-project-team-64/blob/main/architecture_diagram.JPG)








