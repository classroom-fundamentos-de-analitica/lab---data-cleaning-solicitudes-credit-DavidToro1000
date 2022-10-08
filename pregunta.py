"""
Limpieza de datos usando Pandas
-----------------------------------------------------------------------------------------

Realice la limpieza del dataframe. Los tests evaluan si la limpieza fue realizada 
correctamente. Tenga en cuenta datos faltantes y duplicados.

"""
import pandas as pd
import re
from datetime import datetime


def clean_data():

    df = pd.read_csv("solicitudes_credito.csv", sep=";", index_col = 0)
    
    # Se eliminan na y duplicados al inicio para que el programa funcione
    df.dropna(axis=0,inplace=True)
    df.drop_duplicates(inplace = True)

    #Existen datos iguales pero con valores en mayuscula, se corrige esto volviendo todo minuscula
    df["sexo"]=df["sexo"].str.lower()
    df["tipo_de_emprendimiento"]= df["tipo_de_emprendimiento"].str.lower()
    df["idea_negocio"]= df["idea_negocio"].str.lower()
    df["barrio"]= df["barrio"].str.lower()
    df["línea_credito"]= df["línea_credito"].str.lower()

    #Se eliminan los caracteres - y _ de las columnas idea de negocio y barrio para que elimine luego posibles duplicados escritos diferente
    df["idea_negocio"] = df["idea_negocio"].apply(lambda x: x.replace('_', ' '))
    df["idea_negocio"] = df["idea_negocio"].apply(lambda x: x.replace('-', ' '))
    df["barrio"] = df["barrio"].apply(lambda x: x.replace('_', ' '))
    df["barrio"] = df["barrio"].apply(lambda x: x.replace('-', ' '))

    #Monto del credito posee valores que estan escritos como strings, se usa regex para dejarlos en un formato que pueda ser facilmente transformado a entero
    df['monto_del_credito'] = df['monto_del_credito'].apply(lambda x: re.sub("\$[\s*]", "", x))
    df['monto_del_credito'] = df['monto_del_credito'].apply(lambda x: re.sub(",", "", x))
    df['monto_del_credito'] = df['monto_del_credito'].apply(lambda x: re.sub("\.00", "", x))
    df['monto_del_credito'] = df['monto_del_credito'].apply(int)
    
    df['comuna_ciudadano'] = df['comuna_ciudadano'].apply(float)

    #Hay fechas escritas de manera diferente, se transforma entnces en una columna de tipo datetime
    df['fecha_de_beneficio'] = df['fecha_de_beneficio'].apply(lambda x: datetime.strptime(x, "%Y/%m/%d") if (len(re.findall("^\d+/", x)[0]) - 1) == 4 else datetime.strptime(x, "%d/%m/%Y"))

    df.dropna(axis=0,inplace=True)
    # # Se eliminan los registros duplicados
    df.drop_duplicates(inplace = True)

    return df
print(clean_data().sexo.value_counts().to_list())
