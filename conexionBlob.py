from langchain.document_loaders import AzureBlobStorageContainerLoader
import os
from langchain import OpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from Conection import conectPostgres
from langchain import PromptTemplate
from langchain.document_loaders import AzureBlobStorageContainerLoader


# Variables Globales
# german: "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"
openai_api_key = "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"
llm = OpenAI(temperature=0, openai_api_key=openai_api_key)
pdf_directory = 'content/pdf_files'
coneccion, cursor, conection = conectPostgres().ConnectDatabase()

cadena_conexion = "DefaultEndpointsProtocol=https;AccountName=pruebamvp01;AccountKey=9HuLk5/oxma0pZm48fTbEnz6hk4se53+/sIEgshfzCDKOzJLFdCuMVpC/1/TZCaNootI7lYJghN2+AStZJzmIw==;EndpointSuffix=core.windows.net"
contenedor_name =  "pruebamvp01"
container_names = "documentos"



prompt_template = """
                    Escribir un resumen consiso del siguiente texto:
                    {text}
                    Resumen consiso en español:
"""


map_prompt_tem = PromptTemplate(template=prompt_template, input_variables=["text"])


loader = AzureBlobStorageContainerLoader(conn_str=cadena_conexion,
                                          container=container_names)

# Cargue Documentos
docs = loader.load()
print(len(docs))

'''
contador = 0
for page in docs:
    contador = contador+1
    text = page.page_content
    text = text.replace('\t', ' ')
    text = text.strip()

    if (len(page.page_content)== 0):
        print("Este documento no tiene texto")
    
    else:

        print("Numero de Tokens Totales: ",llm.get_num_tokens(text))
        text_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n"], chunk_size=5000, chunk_overlap=500)
        docs = text_splitter.create_documents([text])
        num_docs = len(docs)
        num_tokens_first_doc = llm.get_num_tokens(docs[0].page_content)
        print (f"Now we have {num_docs} documents and the first one has {num_tokens_first_doc} tokens")
        summary_chain = load_summarize_chain(llm=llm, chain_type='map_reduce',map_prompt=map_prompt_tem)
        output = summary_chain.run(docs)
        sumary = output.strip()
        expediente = f"HHMF{contador}"
        nuevo_registro= conectPostgres().insetSummary(expediente, sumary, cursor, conection)

'''