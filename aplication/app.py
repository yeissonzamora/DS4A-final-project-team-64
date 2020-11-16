from flask import Flask
from flask import render_template
import base64
from flask import request
from flask import jsonify
import numpy as np
import pandas as pd
import joblib
import json
from sklearn.tree import DecisionTreeClassifier
import pickle
from sklearn import preprocessing
from sklearn.preprocessing import OneHotEncoder


#Global variables
dl_model = 'modelLog.model'
model = joblib.load(dl_model)
faltantes = {'uni_med_': 1.0,'unidedad': 166.0,'vac_ei': None,'dos_ei': None,'uso_antiv': None,'NOMBRE EPS': 'NUEVA EPS','pac_hos_': 1.0,'uso_antib': None,'tip_ss_': 'C','cod_ase_': 'EPS037','tip_cas_': 2.0,'gp_discapa': 2.0,'gp_desplaz': 2.0,'gp_migrant': 2.0,'gp_carcela': 2.0,'gp_gestan': 2.0,'sem_ges': None,'gp_indigen': 2.0,'gp_pobicbf': 2.0,'gp_mad_com': 2.0,'gp_desmovi': 2.0,'gp_psiquia': 2.0,'gp_vic_vio': 2.0,'gp_otros': 1.0,'ini_sin_': '2020-08-13','fec_con_': '2020-08-17','fec_hos_': '2020-08-18','fec_def_': None,'fec_antiv': '1960-01-01 00:00:00','fec_inguci': '2020-08-18 00:00:00','con_fin_': 1.0}
faltantes = pd.DataFrame([faltantes])   

# API from Flask instance
app = Flask(__name__)


#web page app.route. in this function the html is reder
@app.route('/version2')
def hello_worldv2():
    return render_template("index.html")


#status service
#Is used to test the state of the servers
@app.route('/api/status', methods=['GET'])
def status():
    """
    GET method for API status verification.
    """
    
    message = {
        "status": 200,
        "message": [
            "This API is up and running!"
        ]
    }
    response = jsonify(message)
    response.status_code = 200

    return response

#prediction service
#Is Post service. It recive a json with the data, clean the data, import the model and make the prediction.
@app.route('/api/predict', methods=['POST'])
def predict():
    """
    POST method for emotion prediction endpoint.
    """
    #functions to clean and format the data to use the model. these functions was created in predict.py file and reuse here for make the predition on a unique input.

    def limpiarTodos(data,featgroups,dropColumnsSyC=['vac_ei','dos_ei'],dropSintomasSyC=['der_ple','der_per','falla_resp','septicemia','miocarditi','rinorrea','conjuntivi','cefalea','diarrea'],useAtencion=False,useFechas=False,useGrupos=False,useSocial=False,encode=None,fillEstrato=False,estandarizar=None,scalerFit=True):
        """
        
        Parameters
        ----------
        
        data: DataFrame
            Datos que se van a ingresar
            
        featgroups: dict
            Diccionario con los grupos de características
            
        dropColumnsSyC: object
            default es ['vac_ei','dos_ei']
            
        dropSintomasSyC: object
            default es ['der_ple','der_per','falla_resp','septicemia','miocarditi','rinorrea','conjuntivi','cefalea','diarrea']
        
        useAtencion: boolean
            default es False
            
        useFechas: boolean
            default es False
            
        useGrupos: boolean
            default es False

        useSocial: boolean
            default es False
        
        encode: object
            indica si se van a encodear columnas (deprecado :v)
        
        fillEstrato: boolean
            indica si se van a llenar los estratos en datos faltantes, default es False
        
        estandarizar: object
            default es None
        
        scalerFit: object
            indica si se va el scaler se importa o se ajusta en la función 'None' para ajustarla y cualquier otra cosa para importarlo
        
        """

        SyC=['tos','fiebre','odinofagia','dif_res','adinamia','vac_ei','dos_ei','asma','epoc','diabetes','vih','enf_card','cancer','desnutricion','obesidad','ins_renal','otr_medinm','fumador','tuberculos','hallaz_rad','der_ple','der_per','miocarditi','septicemia','falla_resp','rinorrea','conjuntivi','cefalea','diarrea']
        datos=data.copy()
        datos.dos_ei=datos.dos_ei.fillna(2)
        datos.vac_ei=datos.vac_ei.fillna(2)
        datos.hallaz_rad=datos.hallaz_rad.fillna(4) # Significa que no se aplicó radiografía
        
        if dropColumnsSyC:
            datos=datos.drop(dropColumnsSyC, axis=1)
            
            for elemento in dropColumnsSyC:
                SyC.remove(elemento)
            
        if dropSintomasSyC:
            datos=datos.dropna(subset=dropSintomasSyC)
        else:
            
            datos.der_ple=datos.der_ple.fillna(3) # 3 desconocido
            datos.der_per=datos.der_per.fillna(3) # 3 desconocido
            datos.miocarditi=datos.miocarditi.fillna(3) # 3 desconocido
            datos.septicemia=datos.septicemia.fillna(3) # 3 desconocido
            datos.falla_resp=datos.falla_resp.fillna(3) # 3 desconocido
            datos.rinorrea=datos.rinorrea.fillna(3)# 3 desconocido
            datos.conjuntivi=datos.conjuntivi.fillna(3) # 3 desconocido
            datos.cefalea=datos.cefalea.fillna(3) # 3 desconocido
            datos.diarrea=datos.diarrea.fillna(3) # 3 desconocido

        for columna in SyC:
            datos[columna]=datos[columna].astype(int)

        if useAtencion==False:
            datos=datos.drop(featgroups['Atención'],axis=1)
        if useFechas==False:
            datos=datos.drop(featgroups['Fechas'],axis=1)
        if useGrupos==False:
            datos=datos.drop(featgroups['Grupos'],axis=1)
        if useSocial==False:
            datos=datos.drop(featgroups['Social'],axis=1)
        elif fillEstrato:
            datos.estrato=datos.estrato.fillna(round(datos.estrato.mean(),0))
        
        datos.sexo_=datos.sexo_.apply(lambda xs: 1 if xs=='M' else -1)
        
        def mapEdad(xs):     
            if xs[1]==1:
                return xs[0]*12*30
            elif xs[1]==2:
                return xs[0]*30
            else:
                return xs[0]
        
        datos['edadDias']=datos[['edad_','uni_med_']].apply(lambda xs:mapEdad(xs),axis=1)
        datos=datos.drop(['edad_','uni_med_','unidedad'],axis=1)
         
        datos=datos.dropna().reset_index().drop('index',axis=1)
        
        if not estandarizar is None:
            
            if scalerFit=='None':
                scaler = preprocessing.StandardScaler()
                print('Inicializando scaler')
            else:
                scaler= pickle.load(open( "scalerEdad.p", "rb" ) )
                print('Importando scaler')
            
            datos1=datos[[elemento for elemento in datos.columns if not elemento in estandarizar]]
            datos2=datos[estandarizar]  
            datos1=datos1.reset_index()
            try:
                datos1=datos1.drop('index',axis=1)
            except:
                pass

            datos2=datos2.reset_index()
            try:
                datos2=datos2.drop('index',axis=1)
            except:
                pass

            print(datos1.columns)
            
            if scaler=='None':
                print('Ajustando y transformando')
                datos2=scaler.fit_transform(datos2)
                print('scaler -- mean:{}, var: {}'.format(scaler.mean_,scaler.var_))
            else:
                print('Tranformando')
                datos2=scaler.transform(datos2)
                print('scaler -- mean:{}, var: {}'.format(scaler.mean_,scaler.var_))
            
            #Guardar scaler
            if scaler =='None':
                pickle.dump( scaler, open( "scalerEdad.p", "wb" ) )
            
            datos2=pd.DataFrame(datos2,columns=estandarizar)
            datos=pd.concat([datos1,datos2],axis=1)
        
        datos['ocupacion_Cat']=datos['ocupacion_'].apply(lambda xs: getClaseOcupacion(xs))

        datos=datos.drop('ocupacion_',axis=1)
        datos=datos.drop('con_fin_',axis=1)

        return datos


    def getGroups():
        featgroups={"Paciente":['edad_','sexo_','uni_med_'],"Social":['trab_salud','ocupacion_','estrato']
            ,"Salud":['tos','fiebre','odinofagia','dif_res','adinamia','vac_ei','dos_ei','asma','epoc','diabetes','vih','enf_card','cancer','desnutricion','obesidad','ins_renal','otr_medinm','fumador','tuberculos','hallaz_rad','der_ple','der_per','miocarditi','septicemia','falla_resp','rinorrea','conjuntivi','cefalea','diarrea']
            ,"Atención":['NOMBRE EPS','pac_hos_','uso_antib','uso_antiv','tip_ss_','cod_ase_','tip_cas_']
            ,"Grupos":['gp_discapa','gp_desplaz','gp_migrant','gp_carcela','gp_gestan','sem_ges','gp_indigen','gp_pobicbf','gp_mad_com','gp_desmovi','gp_psiquia','gp_vic_vio','gp_otros']
            ,"Fechas":['ini_sin_','fec_con_','fec_hos_','fec_def_','fec_antiv','fec_inguci']
            ,"Output":['Muerto']
    }
        return featgroups


    def getClaseOcupacion(xs):
        dict_clases={0:'FUERZA PÚBLICA'
                    ,1: 'MIEMBROS DEL PODER EJECUTIVO, DE LOS CUERPOS LEGISLATIVOS Y PERSONAL DIRECTIVO DE LA ADMINISTRACIÓN PÚBLICA Y DE EMPRESAS'
                    ,2:'PROFESIONALES UNIVERSITARIOS, CIENTÍFICOS E INTELECTUALES'
                    ,3: 'TÉCNICOS, POSTSECUNDARIOS NO UNIVERSITARIOS Y ASISTENTES'
                    ,4: 'EMPLEADOS DE OFICINA'
                    ,5: 'TRABAJADORES DE LOS SERVICIOS Y VENDEDORES'
                    ,6: 'AGRICULTORES, TRABAJADORES Y OBREROS AGROPECUARIOS, FORESTALES Y PESQUEROS'
                    ,7: 'OFICIALES, OPERARIOS, ARTESANOS Y TRABAJADORES DE LA INDUSTRIA MANUFACTURERA, DE LA CONSTRUCCIÓN Y DE LA MINERÍA'
                    ,8: 'OPERADORES DE INSTALACIONES, DE MÁQUINAS Y ENSAMBLADORES'
                    ,9: 'TRABAJADORES NO CALIFICADOS'}

        return dict_clases[xs//1000]


    def encodeData(datos,fitted=False):
        
        cats=["sexo_","trab_salud","estrato","tos","fiebre","odinofagia","dif_res"
                                            ,"adinamia","asma","epoc","diabetes","vih","enf_card","cancer","desnutricion",
                                            "obesidad","ins_renal","otr_medinm","fumador","tuberculos","miocarditi","hallaz_rad",'der_ple', 'der_per', 'septicemia', 'falla_resp',
        'rinorrea', 'conjuntivi', 'cefalea', 'diarrea','ocupacion_Cat']

        splitA=datos[cats]
        splitB=datos[[columna for columna in datos.columns if not columna in cats]]

        if fitted==False:
            print("Ajustando")
            enc=OneHotEncoder(handle_unknown='ignore')
            enc.fit(splitA)
            pickle.dump( enc, open( "encoderCats.p", "wb" ) )   
        elif fitted==True:
            print("Importando")
            enc= pickle.load(open( "encoderCats.p", "rb" ) ) 
        else:
            raise "Envíe algo >:v"
            
        print("Transformando")
        enc.transform(splitA).toarray().shape

        fittedencodedData=pd.DataFrame(enc.transform(splitA).toarray().T,list(enc.get_feature_names())).T 
        
        assert fittedencodedData.shape[1]==84, "El output no es correcto"
        
        fittedencodedData=pd.concat([splitB,fittedencodedData],axis=1)
        
        return fittedencodedData

    # Get data as JSON from POST
    data = request.get_json()
    # Convert a data in a dataframe
    entrada = pd.DataFrame([data])
    #Concat the tha data input with the faltantes dataset. In order to re usea the functions. The fields of faltantes dataset wiil be deleted in clean process
    datos = pd.concat([entrada,faltantes], axis= 1)
    featgroups=getGroups()
    #Clean data
    print("Limpiando datos")
    datosB=limpiarTodos(datos,featgroups,useSocial=True,fillEstrato=True,estandarizar=['edadDias'],scalerFit=True)
    #Encode data
    datos_=encodeData(datosB,fitted=True)
    # Predict using  model
    print("Realizando predicción")
    prediction = model.predict_proba(datos_)[0][1]
    # Send response
    message = {
        "status": 200,
        "message": [
            {
                "task": "Prediction Transaction",
                "prediction": str(prediction)
            }
        ]
    }
    response = jsonify(message)
    response.status_code = 200

    return response

#Service to handle the error
@app.errorhandler(404)
def not_found(error=None):
    """
    GET method for not found routes.
    """
    
    message = {
        "status": 404,
        "message": [
            "[ERROR] URL not found."
        ]
    }
    response = jsonify(message)
    response.status_code = 404
    
    return response


if __name__ == "__main__":
    app.run(debug=True)
    #app.run(host='0.0.0.0', port=5000)


