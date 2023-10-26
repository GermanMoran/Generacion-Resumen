import os
from langchain import OpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
import tiktoken


# Se define el promt template
prompt_template = """
Escribir un resumen consiso del siguiente texto:
{text}
Resumen consiso en español:"""


prompt = PromptTemplate(template=prompt_template, input_variables=["text"])
openai_api_key = "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"

# Se carga el libro
loader = PyPDFLoader("content/pdf_files/Durmiente.pdf")
pages = loader.load()

print(pages)

# Se define el modelo de lenguaje
model_name= "gpt-3.5-turbo"
llm = OpenAI(temperature=0, openai_api_key=openai_api_key, model_name=model_name)

docs = [page for page in pages]
print(docs)


text = ""
for page in pages:
    text += page.page_content
    
text = text.replace('\t', ' ')


def num_tokens_from_string(string: str, encoding_name: str) -> int:    
    encoding = tiktoken.encoding_for_model(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

num_tokens = num_tokens_from_string(text, model_name)
print(num_tokens)



model_max_tokens = 4097
verbose = True

if num_tokens < model_max_tokens:
  chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt, verbose=verbose)
else:
  chain = load_summarize_chain(llm, chain_type="map_reduce", map_prompt=prompt, combine_prompt=prompt, verbose=verbose)

#start_time = monotonic()
summary = chain.run(docs)
print(summary)


with open(f'content/extracted_text/resumen.txt', 'w') as out:
            out.write(summary)



'''
print(f"Chain type: {chain.__class__.__name__}")
print(f"Run time: {monotonic() - start_time}")
print(f"Summary: {textwrap.fill(summary, width=100)}")

'''