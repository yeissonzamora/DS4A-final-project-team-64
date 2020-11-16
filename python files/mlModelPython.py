import joblib

import pandas as pd

cats=["sexo_","trab_salud","estrato","tos","fiebre","odinofagia","dif_res"
                                          ,"adinamia","asma","epoc","diabetes","vih","enf_card","cancer","desnutricion",
                                          "obesidad","ins_renal","otr_medinm","fumador","tuberculos","miocarditi","hallaz_rad",'der_ple', 'der_per', 'septicemia', 'falla_resp',
       'rinorrea', 'conjuntivi', 'cefalea', 'diarrea','ocupacion_Cat']


def getData(input_type,direccion,filtrarDescesos=True):
    """
    Función para cargar los datos
    
    Parameters
    ----------
    
    input_type: str
        Forma en la que se realizará la carga de los datos puede ser: 'base' para 
    cargar desde la conexión a postgresql o 'archivo' para cargar desde excel
    
    direccion: str
        Opcional para input_type='archivo'
    
    filtrarDescesos: boolean
        permite realizar el filtro según el grupo de pacientes que tuvieron descenlace o no.
    
    """
    if input_type=='archivo':
        
        data=pd.read_excel(direccion)
        
    
    elif input_type=='base':
        #
        from sqlalchemy import create_engine
        
        engine=create_engine('postgresql://postgres:ds4abucaramanga@bucaramanga-ds4a.clf0f3kzvlpj.us-east-1.rds.amazonaws.com:5432/postgres')
        
        data=pd.read_sql('SELECT * FROM coronavirus', engine)
        
        data.ocupacion_=data.ocupacion_.astype('float64')
        data.ocupacion_=data.ocupacion_.astype('float64')
        data.estrato =data.estrato.astype('float64')
    
    
    if filtrarDescesos==True:
        
        datosFiltrados=data.copy()
        #datosFiltrados.ajuste_=datosFiltrados.ajuste_.astype(int)
        datosFiltrados.serv_hosp=datosFiltrados.serv_hosp.astype(int)
        
        datosFiltrados=datosFiltrados[datosFiltrados.ajuste_=='3']
        #{3:'In UCI', 5:'Death', 1:'In hospital', 4:'recovered', 2:'At home', 6:'No COVID Death' }

        datosFiltrados=datosFiltrados[datosFiltrados.serv_hosp!=4]
        datosFiltrados=datosFiltrados[datosFiltrados.serv_hosp!=5]
        datosFiltrados=datosFiltrados[datosFiltrados.serv_hosp!=6]       
        
        datosFiltrados=datosFiltrados[['edad_','sexo_','uni_med_','unidedad','trab_salud','ocupacion_','estrato','tos','fiebre','odinofagia','dif_res','adinamia','vac_ei','dos_ei','asma','epoc','diabetes','vih','enf_card','cancer','desnutricion','obesidad','ins_renal','otr_medinm','fumador','tuberculos','hallaz_rad','uso_antiv','der_ple','der_per','miocarditi','septicemia','falla_resp','rinorrea','conjuntivi','cefalea','diarrea','NOMBRE EPS','pac_hos_','uso_antib','tip_ss_','cod_ase_','tip_cas_','gp_discapa','gp_desplaz','gp_migrant','gp_carcela','gp_gestan','sem_ges','gp_indigen','gp_pobicbf','gp_mad_com','gp_desmovi','gp_psiquia','gp_vic_vio','gp_otros','ini_sin_','fec_con_','fec_hos_','fec_def_','fec_antiv','fec_inguci','con_fin_']]
        
        data=datosFiltrados
        
        return data

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
    
    
    import pickle
    from sklearn import preprocessing
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
    
    import pickle
    
    cats=["sexo_","trab_salud","estrato","tos","fiebre","odinofagia","dif_res"
                                          ,"adinamia","asma","epoc","diabetes","vih","enf_card","cancer","desnutricion",
                                          "obesidad","ins_renal","otr_medinm","fumador","tuberculos","miocarditi","hallaz_rad",'der_ple', 'der_per', 'septicemia', 'falla_resp',
       'rinorrea', 'conjuntivi', 'cefalea', 'diarrea','ocupacion_Cat']
    
    from sklearn.preprocessing import OneHotEncoder


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


def inverseTransform(datos_):
    import pickle
    datos=datos_.copy()
    datos.sexo_=datos.sexo_.apply(lambda xs: 'M' if xs==1 else 'F')
    scaler= pickle.load(open( "scalerEdad.p", "rb" ) )
    datos.edadDias=scaler.inverse_transform(datos.edadDias)/(30*12)
    datos=datos.rename(columns={'edadDias':'edad'})
    return datos

def cargarPostgreSQL(nombreTablaDestino,tabla):
    from sqlalchemy import create_engine
    engineOut=create_engine('postgresql://postgres:ds4abucaramanga@bucaramanga-ds4a.clf0f3kzvlpj.us-east-1.rds.amazonaws.com:5432/postgres')
    print("Engine Correcto")
    tabla.to_sql(nombreTablaDestino,engineOut,index=False,if_exists='replace')
    print("")
    
    
    
#Cargar
#Preprocesar datos

def main():
    print("Cargando datos")
    datos=getData('base','')
    featgroups=getGroups()
    print("Limpiando datos")
    datosB=limpiarTodos(datos,featgroups,useSocial=True,fillEstrato=True,estandarizar=['edadDias'],scalerFit=True)
    datos_=encodeData(datosB,fitted=True)
    #Cargar modelo
    print("Cargando modelo")
    model = joblib.load('modelLog.model')

    #Realizar prediccion
    print("Realizando predicción")
    df=pd.DataFrame(model.predict_proba(datos_),columns=['ProbabilidadVivir','ProbabilidadMorir'])
    df['class']=model.predict(datos_)
    df_final=pd.concat([inverseTransform(datosB),df],axis=1)
    #Cargar a PostgreSQL
    print("Cargando a db")
    cargarPostgreSQL('TablaIntento',df_final)
    
    
    
if __name__=="__main__":
    main()