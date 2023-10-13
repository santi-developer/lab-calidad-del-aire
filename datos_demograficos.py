import pandas as pd
from typing import Set
import requests

def ej_1_cargar_datos_demograficos() -> pd.DataFrame:
    d_demograficos=pd.read_csv("us-cities-demographics.csv", sep=';', encoding='utf-8')
    print(d_demograficos)
    return d_demograficos

def conseguirset(df)->set:
    ciudades=set(df['City'])
    print(ciudades)
    return ciudades

def  ej_2_cargar_calidad_aire(ciudades):
    lista_ciudades=list(ciudades)
    quality_data = []
    for ciudad in lista_ciudades:
        
        api_url = f'https://api.api-ninjas.com/v1/airquality?city={ciudad}'
        
        try:
            response = requests.get(api_url, headers={'X-Api-Key': 'P/iKNbaCS6v6TTiCOX0aPA==ylf11BlFYvQJd2lQ'}, timeout=10)
            if response.status_code == requests.codes.ok:
                data = response.json()
                quality_data.append(data)
                print(data)
                print(type(data))
                
            else:
                print(f"Error al obtener datos para {ciudad}: {response.status_code}")
                lista_ciudades.remove(ciudad)
                
        except requests.exceptions.Timeout:
            print(f"Tiempo de espera agotado al conectar con la API para {ciudad}")
            lista_ciudades.remove(ciudad)
            
        except requests.exceptions.RequestException as e:
            print(f"Error al realizar la solicitud a la API para {ciudad}: {str(e)}")
            lista_ciudades.remove(ciudad)
            
        
        
    # Inicializa el diccionario final
    nuevo_formato = {}

    for i, diccionario in enumerate(quality_data):
        for contaminante, valores in diccionario.items():
            if isinstance(valores, dict):
                if 'concentration' in valores:
                    valor_concentracion = valores['concentration']
                else:
                    valor_concentracion = valores  # Utiliza el valor directo
                if contaminante not in nuevo_formato:
                    nuevo_formato[contaminante] = {}
                nuevo_formato[contaminante][i] = valor_concentracion
                
    new=pd.DataFrame(nuevo_formato)
    dictionary=new.to_dict()
            
    print(new)
    print(dictionary)
    
    
cargar=ej_1_cargar_datos_demograficos()
data=conseguirset(cargar)
ej_2_cargar_calidad_aire(data)
            
        
        
