import os
from langchain import OpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain import PromptTemplate
from langchain.document_loaders import AzureBlobStorageContainerLoader
from langchain.document_loaders import AzureBlobStorageContainerLoader
from dotenv import load_dotenv
from ConectionPostgres import conectPostgres
from ElasticSearch import ElasticSearch
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from langchain.document_loaders import AzureBlobStorageFileLoader



# Cargue Variables Globales
load_dotenv()
openai_key = os.getenv('API_KEY_OPENIA')
container_name = os.getenv('CONTAINER_NAME')
string_conection = os.getenv('CONNECTION_STRING_BLOB_STORAGE')
server = os.getenv('SERVER_ELASTIC_NAME')
index_name = os.getenv('INDEX_NAME')
elastic_conection = ElasticSearch(server).connect_elasticsearch()

container = ContainerClient.from_connection_string(conn_str=string_conection, container_name=container_name)


# Modelo de Lenguage
llm = OpenAI(temperature=0, openai_api_key=openai_key)
prompt_template = """
                    Escribir un resumen consiso del siguiente texto:
                    {text}
                    Resumen consiso en español:
"""
# Prompt para obtener resumen documento
map_prompt_tem = PromptTemplate(template=prompt_template, input_variables=["text"])


contador = 0
#docs = []
blob_list = container.list_blobs()
for blob in blob_list:
    ex = blob.name.split(".")
    if ex[len(ex)-1] == "pdf":
        contador = contador +1
        #blob_client = container.get_blob_client(blob.name)
        #r = blob_client.download_blob().readall()
        try:
            loader = AzureBlobStorageFileLoader(conn_str= string_conection,
                                                container=container_name,
                                                blob_name=blob.name)
            doc = loader.load()

            text = doc[0].page_content
            text = text.replace('\t', ' ')
            text = text.strip()

            if (len(doc[0].page_content)== 0):
                print("Este documento no tiene texto")
        
            else:

                expediente = f"EXPEDP{contador}"
                # Resumen del texto  - OpenAI
                print("Numero de Tokens Totales: ",llm.get_num_tokens(text))
                print(len(text))
                
                text_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n"], chunk_size=4000, chunk_overlap=500)
                docs = text_splitter.create_documents([text])
                num_docs = len(docs)
                num_tokens_first_doc = llm.get_num_tokens(docs[0].page_content)
                print (f"Now we have {num_docs} documents and the first one has {num_tokens_first_doc} tokens")
                summary_chain = load_summarize_chain(llm=llm, chain_type='map_reduce',map_prompt=map_prompt_tem)
                output = summary_chain.run(docs)
                sumary = output.strip()

                data = {
                    "Expediente": expediente,
                    "texto": text,
                    "Resumen": sumary
                }

                save_record = ElasticSearch(server).store_record(es_object=elastic_conection,index=index_name, data=data)
                print(save_record)
        except:
            print("Error cargar documento - Documento cifrado")
            
    else:
        print("No PDF")
    







