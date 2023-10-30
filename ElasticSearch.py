# Librerias y Dependencias
import json
from elasticsearch import Elasticsearch


class ElasticSearch():
    def __init__(self, servidor):
        self.servidor = servidor

    # Funcion para crear un index en caso de que no exista

    def connect_elasticsearch(self):
        _es = None
        _es = Elasticsearch(self.servidor)
        if _es.ping():
            print('Servidor conectado')
        else:
            print('No se puede conectar con el servidor')
        return _es


    def store_record(self, es_object, index, data):
        is_stored = True

        try:
            outcome = es_object.index(index=index,  body=json.dumps(data))
            print(outcome)
        except Exception as ex:
            print('Error  al indexar las data')
            print(str(ex))
            is_stored = False
        finally:
            return is_stored




'''
if __name__ == '__main__':

    es = connect_elasticsearch()
    
    cadena = "Diego fernando moran figueroa es ingeniero agroindustrial de la universidad Nacional de colombia"
    data = {
        "Expediente": "ES",
        "Resumen": cadena
    }
    r = store_record(es, 'company', data)
    print(r)

'''