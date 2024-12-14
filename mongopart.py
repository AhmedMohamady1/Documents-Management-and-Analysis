from pymongo import MongoClient
from gridfs import GridFS
from PyPDF2 import PdfReader
from docx import Document
import win32com.client
import os

client= MongoClient()
db= client.Project
collection= db["PDFS"]
fs = GridFS(db)

def insert_file(file):
    existing_file = collection.find_one({"name": file["name"]})
    if existing_file:
        print("File already exists in the database.")
    else:
        result = collection.insert_one(file)
        if result.inserted_id:
            print(f"File inserted successfully with ID: {result.inserted_id}")
        else:
            print("Failed to insert the File.")

def delete_file(file_name):
    filter_criteria = {"name": file_name}
    
    result = collection.delete_one(filter_criteria)
    if result.deleted_count > 0:
        print(f"File '{file_name}' deleted successfully.")
    else:
        print(f"No file matched the name '{file_name}'.")

def get_word_page_count(word_data):
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False  
    
    temp_path = "temp_document.docx"
    with open(temp_path, "wb") as temp_file:
        temp_file.write(word_data)
    
    doc = word.Documents.Open(os.path.abspath(temp_path))

    page_count = doc.ComputeStatistics(2)
    
    doc.Close()
    word.Quit()
    os.remove(temp_path)
    
    return page_count


def count_pages(file_path, file_data):
    file_extension = os.path.splitext(file_path)[1].lower()
    
    if file_extension == ".pdf":
        with open(file_path, "rb") as pdf_file:
            pdf_reader = PdfReader(pdf_file)
            return len(pdf_reader.pages)
        
    elif file_extension == ".docx":
        return get_word_page_count(file_data)

    elif file_extension == ".txt":
        return 1
    
    else:
        raise ValueError("Unsupported file format. Only .pdf and .docx files are supported.")

def extract_text_from_docx(file_path):
        text = ""
        document = Document(file_path)
        for paragraph in document.paragraphs:
            text += paragraph.text
        return text

def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PdfReader(file)
        text = ''
        for page in range(len(reader.pages)):
            text += reader.pages[page].extract_text()
        return text

def extract_text_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def extract_text_from_generic(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        return file.read()


def extract_text_from_file(file_path):
    # Check if the file exists
    if not os.path.isfile(file_path):
        return f"File not found: {file_path}"
    
    # Get the file extension
    file_extension = os.path.splitext(file_path)[1].lower()
    
    try:
        # Handle PDF files
        if file_extension == ".pdf":
            return extract_text_from_pdf(file_path)
        
        # Handle DOCX files
        elif file_extension == ".docx":
            return extract_text_from_docx(file_path)
        
        # Handle TXT files
        elif file_extension == ".txt":
            return extract_text_from_txt(file_path)
        
        # Handle generic files
        else:
            return extract_text_from_generic(file_path)
    
    except Exception as e:
        return f"Error processing file: {e}"

def count_words_in_text(text):
    words = text.split()
    return len(words)

def count_characters_in_text(text, include_newlines=True):
    if not include_newlines:
        text = text.replace('\n', '')
    return len(text)

def Pull_File(file_path):
    text=extract_text_from_file(file_path)
    with open(file_path, "rb") as file:
        data = file.read()
        document = {
            "name": file_path.split("/")[-1],
            "contents": text,
            "file_data": data,
            "pages": count_pages(file_path, data),
            "words": count_words_in_text(text),
            "characters": count_characters_in_text(text),
            "modify date":datetime.fromtimestamp(os.path.getmtime(file_path)),
            "upload date":datetime.now()
        }
        insert_file(document)

def download_pdf(file_name, save_path):
    document = collection.find_one({"name": file_name})
    if not document:
        print(f"No file found with the name: {file_name}")
        return
    
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    with open(save_path, "wb") as file:
        file.write(document["file_data"])
    
    print(f"file downloaded successfully to {save_path}")

