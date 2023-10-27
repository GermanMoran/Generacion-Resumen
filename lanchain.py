
## Librerias y dependencias
import os
from langchain import OpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from Conection import conectPostgres
from langchain import PromptTemplate
from langchain.document_loaders import AzureBlobStorageContainerLoader



prompt_template = """
Escribir un resumen consiso del siguiente texto:
{text}
Resumen consiso en español:"""


map_prompt = PromptTemplate(template=prompt_template, input_variables=["text"])



# Claves
openai_api_key = "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"
# Modelo de Lenguaje
llm = OpenAI(temperature=0, openai_api_key=openai_api_key)
loader = PyPDFLoader("content/pdf_files/Himno.pdf")
pages = loader.load()




# Conecccion BD
coneccion, cursor, conection = conectPostgres().ConnectDatabase()


text = ""
for page in pages:
    text += page.page_content


text = text.replace('\t', ' ')
#text = text.replace('\n', ' ')
text = text.strip()


with open(f'content/extracted_text/text.txt', 'w') as out:
            out.write(text)



print("Numero de Tokens Totales: ",llm.get_num_tokens(text))
text_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n"], chunk_size=5000, chunk_overlap=500)
docs = text_splitter.create_documents([text])
num_docs = len(docs)

num_tokens_first_doc = llm.get_num_tokens(docs[0].page_content)
print (f"Now we have {num_docs} documents and the first one has {num_tokens_first_doc} tokens")


summary_chain = load_summarize_chain(llm=llm, chain_type='map_reduce', map_prompt=map_prompt)
output = summary_chain.run(docs)
sumary = output.strip()



with open(f'content/Summarys/resumen.txt', 'w') as out:
            out.write(sumary)


print(output)


'''
nuevo_registro= conectPostgres().insetSummary("GHMF", sumary, cursor, conection)

'''

