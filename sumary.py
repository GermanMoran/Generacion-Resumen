import os
import PyPDF2
from PyPDF2 import PdfReader
from PIL import Image
import pytesseract
from transformers import T5ForConditionalGeneration,T5Tokenizer
import torch


# Directory for storing PDF resumes and job applications
pdf_directory = 'content/pdf_files'

# Directory for storing extracted text from PDFs
text_directory = 'content/extracted_text'

# OCR output directory for scanned PDFs
ocr_directory = 'content/ocr_output'


print("hola")




resume_files = []
for file_name in os.listdir(pdf_directory):
    print(file_name)
    if file_name.endswith('.pdf'):
        resume_files.append(os.path.join(pdf_directory, file_name))

print(resume_files)
resume_summaries = []  # To store the generated summaries

resume_fileses = ['content/pdf_files/ATRAVESDELESPEJO.pdf', 'content/pdf_files/BLANCANIEVES.pdf', 'content/pdf_files/CV_GERMAN_DATA_ES.pdf']
# Loop through each resume file
for resume_file in resume_files:
    with open(resume_file, 'rb') as file:
        # Create a PDF reader object
        reader = PyPDF2.PdfReader(file)

        # Extract text from each page
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    
    

    # Initialize the model and tokenizer
    model = T5ForConditionalGeneration.from_pretrained("t5-base")
    tokenizer = T5Tokenizer.from_pretrained("t5-base")

    # Encode the text
    inputs = tokenizer.encode("summarize: " + text, 
    return_tensors="pt", max_length=1000, 
    truncation=True)

    # Generate the summary
    outputs = model.generate(inputs, 
    max_length=1000, min_length=100, 
    length_penalty=2.0, num_beams=4, 
    early_stopping=True)

    # Decode the summary
    summary = tokenizer.decode(outputs[0])

    resume_summaries.append(summary)

# Print the generated summaries for each resume
for i, summary in enumerate(resume_summaries):
    print(f"Summary for Resume {i+1}:")
    print(summary)
    print()

#print(text)



