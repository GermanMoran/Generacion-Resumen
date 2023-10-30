from typing import Union
from fastapi import FastAPI
from ElasticSearch import ElasticSearch
app = FastAPI()



# Conexion con ElasticSearch
server = "http://localhost:9200"
index_name = "company"
es = ElasticSearch(server).connect_elasticsearch()



@app.get("/")
def read_root():
    return {"Hello": "World"}


# Primer metodo busqueda de palabras | cadenas de texto elasticsearch
@app.get("/items/search")
def search(query:str):
    script_query = {"match": {"texto":query}}
    search_results = es.search(index=index_name, body={"query": script_query})
    results = search_results["hits"]["hits"]
    return {"results": [ x["_source"]["Expediente"] for x in results]}


# Segundo metodo | Obtener resumen de acuerdo al IDEXPEDIENTE del documento
@app.get("/items/search_id")
def search_id(id:str):
    script_query = {"match": {"Expediente":id}}
    search_results = es.search(index=index_name, body={"query": script_query})
    list_results = search_results["hits"]["hits"]
    if (len(list_results)==0):
        return {"results": ""}
    else:
        return {"results": list_results[0]["_source"]["Resumen"]}
        



