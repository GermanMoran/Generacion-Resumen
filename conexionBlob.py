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

# Cargue Variables Globales
load_dotenv()
openai_key = os.getenv('API_KEY_OPENIA')
container_name = os.getenv('CONTAINER_NAME')
string_conection = os.getenv('CONNECTION_STRING_BLOB_STORAGE')
server = os.getenv('SERVER_ELASTIC_NAME')
index_name = os.getenv('INDEX_NAME')
elastic_conection = ElasticSearch(server).connect_elasticsearch()


#llm = OpenAI(temperature=0, openai_api_key=openai_key)
#coneccion, cursor, conection = conectPostgres().ConnectDatabase()
prompt_template = """
                    Escribir un resumen consiso del siguiente texto:
                    {text}
                    Resumen consiso en español:
"""
#map_prompt_tem = PromptTemplate(template=prompt_template, input_variables=["text"])


loader = AzureBlobStorageContainerLoader(conn_str=string_conection,
                                          container=container_name,
                                          prefix="Hx")

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

        expediente = f"EXPED{contador}"
        data = {
            "Expediente": expediente,
            "Resumen": text
        }

        save_record = ElasticSearch(server).store_record(es_object=elastic_conection,index=index_name, data=data)
        print(save_record)


        
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

