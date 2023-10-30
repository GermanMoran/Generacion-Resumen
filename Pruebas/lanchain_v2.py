
## Librerias y dependencias
import os
from langchain import OpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from Conection import conectPostgres

from langchain.document_loaders import AzureBlobStorageContainerLoader


# Variables Globales
# german: "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"
openai_api_key = "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"
llm = OpenAI(temperature=0, openai_api_key=openai_api_key)
pdf_directory = 'content/pdf_files'
coneccion, cursor, conection = conectPostgres().ConnectDatabase()



resume_files = []
for file_name in os.listdir(pdf_directory):
    print(file_name)
    if file_name.endswith('.pdf'):
        resume_files.append(os.path.join(pdf_directory, file_name))


print(resume_files)



contador = 0
for doc in resume_files:
    contador=contador+1
    loader = PyPDFLoader(doc)
    pages = loader.load()

    text = ""
    for page in pages:
        text += page.page_content


    text = text.replace('\t', ' ')
    text = text.strip()


    with open(f'content/extracted_text/text{contador}.txt', 'w', encoding="utf-8") as out:
                out.write(text)


    print("Numero de Tokens Totales: ",llm.get_num_tokens(text))
    text_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n"], chunk_size=5000, chunk_overlap=500)
    docs = text_splitter.create_documents([text])
    num_docs = len(docs)
    num_tokens_first_doc = llm.get_num_tokens(docs[0].page_content)
    print (f"Now we have {num_docs} documents and the first one has {num_tokens_first_doc} tokens")
    summary_chain = load_summarize_chain(llm=llm, chain_type='map_reduce')
    output = summary_chain.run(docs)
    sumary = output.strip()



    with open(f'content/Summarys/resumen{contador}.txt', 'w', encoding="utf-8") as out:
                out.write(sumary)

    
    expediente = f"ABCD{contador}"
    nuevo_registro= conectPostgres().insetSummary(expediente, sumary, cursor, conection)


