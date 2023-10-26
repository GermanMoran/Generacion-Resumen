# Principales librerias y dependencias
import os
import PyPDF2
from PyPDF2 import PdfReader
from PIL import Image
import pytesseract
import openai
import time

# Funciones
def get_completion(prompt, model="gpt-3.5-turbo"):
  messages = [{"role": "user", "content": prompt}]
  response = openai.ChatCompletion.create(
     model=model,
     messages=messages,
     temperature=0,
  )
  return response.choices[0].message["content"]
    

# Directorios Almacenar texto
pdf_directory = 'content/pdf_files'
text_directory = 'content/extracted_text'
ocr_directory = 'content/ocr_output'


# Variables Globales
openai.api_key  = "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"

resume_files = []
for file_name in os.listdir(pdf_directory):
    print(file_name)
    if file_name.endswith('.pdf'):
        resume_files.append(os.path.join(pdf_directory, file_name))

print(resume_files)

# Almacenar Resumenes
resume_summaries = [] 
text=[]
summary=''
# Ciclo para extarer texto c/d pdf
contador = 0
for resume_file in resume_files:
    contador=contador+1
    with open(resume_file, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        #text = ''
        text = []
        for page in reader.pages:
            pobjet = page.extract_text()
            #text += page.extract_text()
            #text.replace('\t\r','')
            #text.replace('\xa0','')
            text.append(pobjet)
        
        # Guardo el texto extraido pdf
        #with open(f'content/extracted_text/text_{contador}.txt', 'w') as out:
        #    out.write(text)

        
        for i in range(len(text)):
            prompt =f"""
                input Language: Spanish
                Your task is to extract relevant information from a text. This information will be used to create a book summary.
                Extract relevant information from the following text, which is delimited with triple backticks.\
                Be sure to preserve the important details.
                output Language: Spanish
                Text: ```{text[i]}```
            """
            try:
                response = get_completion(prompt)
            except:
                response = get_completion(prompt)

            print(response)
            summary= summary+' ' +response +'\n\n'
            #time.sleep(19)
            resume_summaries.append(response)
            
            # Guardo el resumen en archivo txt
            with open(f'content/resume_output/summary{contador}.txt', 'w') as out:
                out.write(summary)
            
        





    

    