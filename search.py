from pymongo import MongoClient
from gridfs import GridFS
from PyPDF2 import PdfReader
import os
from datetime import datetime, timedelta

client= MongoClient()

local= client.Project
collection= local["documents"]
fs = GridFS(local)
        
def insert_file(file):
    existing_file = collection.find_one(file)
    if existing_file:
        print("File already exists in the database.")
    else:
        document = collection.insert_one(file)
        if document.inserted_id:
            print(f"File inserted successfully with ID: {document.inserted_id}")
        else:
            print("Failed to insert the File.")
            
def count_pdf_pages(file_path):
    with open(file_path, "rb") as pdf_file:
        pdf_reader = PdfReader(pdf_file)
        return len(pdf_reader.pages)

def extract_text_from_pdf(file):
    try:
        reader = PdfReader(file)
        text = ''
        for page in range(len(reader.pages)):
            text += reader.pages[page].extract_text()
        return text
    except FileNotFoundError:
        print(f"The file {file} does not exist.")
        return ''

def count_words_in_text(text):
    words = text.split()
    return len(words)

def count_characters_in_text(text, include_newlines=True):
    if not include_newlines:
        text = text.replace('\n', '')
    return len(text)

def Pull_File(file_path):
    text=extract_text_from_pdf(file_path)
    with open(file_path, "rb") as pdf_file:
        pdf_data = pdf_file.read()
        document = {
            "name": file_path.split("/")[-1],
            "file": pdf_data,
            "pages": count_pdf_pages(file_path),
            "words": count_words_in_text(text),
            "characters": count_characters_in_text(text),
            "date created":datetime.datetime.fromtimestamp(os.path.getctime(file_path)),
        }
        insert_file(document)

def download_pdf(file_name, save_path):
    document = collection.find_one({"name": file_name})
    if not document:
        print(f"No file found with the name: {file_name}")
        return
    
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    with open(save_path, "wb") as pdf_file:
        pdf_file.write(document["file"])
    
    print(f"PDF downloaded successfully to {save_path}")
from nltk.corpus import stopwords
import nltk
from collections import Counter
import re

class Search:
    def __init__(self, mongodb_driver):
        self.__mongodb_driver=mongodb_driver
    
    def __db_query(self, term: str, attribute: str):
        if attribute not in ['name','contents','modify date','upload date']:
            return
        projection={'_id':0}
        if attribute=='upload date' or attribute=='modify date':
            date=term.split('-')
            date=datetime(int(date[0]),int(date[1]),int(date[2]))
            start_of_day = date
            end_of_day = date + timedelta(days=1)
            search_term={attribute: {"$gte": start_of_day,"$lt": end_of_day}}
        else:
            search_term={attribute: {"$regex": term, "$options": "i"}}
        return list(self.__mongodb_driver.find(search_term,projection))
    
    def __print_document(self, document):
        print(f'Name: {document['name'].split('.')[0]}\nType: {document['name'].split('.')[-1]}\nNo. of Pages: {document['pages']}\nNo. of Words: {document['words']}\nNo. of Characters: {document['characters']}\nDate Uploaded: {str(document['upload date']).split('.')[0]}')
            
    def __most_common_words(self, words_list: list, n=5):
        word_counts = Counter(words_list)
        
        most_common = word_counts.most_common(n)
        
        print('\nMost commonly used words:\n')
        for i in range(len(most_common)):
            print(f'{i+1}) {most_common[i][0].title()} : {most_common[i][1]}')
            
    def __term_frequency(self, search_term, content):
        words = self.__remove_unnecessary_words(content)
        for i in range(len(words)):
            words[i]=words[i].lower()
        return round(words.count(search_term.lower())/len(words),6)
    
    def __remove_unnecessary_words(self,input_string):
        stop_words = set(stopwords.words('english'))
        words = input_string.split()

        filtered_words = [
            re.sub(r'[^a-zA-Z]', '', word)
            for word in words
            if word.lower() not in stop_words and re.sub(r'[^a-zA-Z]', '', word)
        ]
        
        return filtered_words
        
    def search_file(self, search_term: str, attribute: str):
        try:
            documents = self.__db_query(search_term,attribute)
            if len(documents)==0:
                print('Document not found.')
                return
            for document in documents:
                self.__print_document(document)
                self.__most_common_words(self.__remove_unnecessary_words(document['contents']))
                print('=================================================================')
        except Exception as e:
            print('Query error:',e)
    
    def search_contents(self, search_term: str):
        try:
            documents = self.__db_query(search_term, 'contents')
            if len(documents)==0:
                print('Document not found.')
                return
            print(f'Documents that contain {search_term.title()}')
            for document in documents:
                self.__print_document(document)
                print(f'Term Frequency of {search_term}: {self.__term_frequency(search_term, document['contents'])}')
                print('=================================================================')
        except Exception as e:
            print('Query error:',e)
    

        
if __name__=='__main__':
    search=Search(collection)
    search.search_contents('Final')
