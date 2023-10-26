
import os
from langchain import OpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter

openai_api_key = "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"
# Load the book
loader = PyPDFLoader("content/pdf_files/Cenicienta.pdf")
pages = loader.load()

# Se define el modelo de lenguaje
llm = OpenAI(temperature=0, openai_api_key=openai_api_key)

text = ""
for page in pages:
    text += page.page_content

    
text = text.replace('\t', ' ')
#text = text.replace('\n', ' ')
text = text.strip()
print(text)

with open(f'content/extracted_text/text.txt', 'w') as out:
            out.write(text)



print("Numero de Tokens Totales: ",llm.get_num_tokens(text))
text_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n"], chunk_size=5000, chunk_overlap=500)
docs = text_splitter.create_documents([text])
num_docs = len(docs)

num_tokens_first_doc = llm.get_num_tokens(docs[0].page_content)

print (f"Now we have {num_docs} documents and the first one has {num_tokens_first_doc} tokens")


summary_chain = load_summarize_chain(llm=llm, chain_type='map_reduce')
output = summary_chain.run(docs)
print(output)


