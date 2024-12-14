from nltk.corpus import stopwords
import nltk
from collections import Counter
import re
import fitz
from datetime import datetime,timedelta


class Search:
    def __init__(self, mongodb_driver):
        self.__mongodb_driver=mongodb_driver

    def __db_query(self, search_terms, attributes='contents'):
        # Ensure attributes are valid
        valid_attributes = ['name', 'contents', 'modify date', 'upload date']
        
        # Convert single strings to lists
        if isinstance(search_terms, str):
            search_terms = [search_terms]
        if isinstance(attributes, str):
            attributes = [attributes]

        if not all(attr in valid_attributes for attr in attributes):
            return

        # Initialize the query
        search_queries = []
        for i in range(len(attributes)):
            if attributes[i] in ['upload date', 'modify date']:
                try:
                    # Parse date
                    date_parts = search_terms[i].split('-')
                    date = datetime(int(date_parts[0]), int(date_parts[1]), int(date_parts[2]))
                    start_of_day = date
                    end_of_day = date + timedelta(days=1)

                    # Add to search queries
                    search_queries.append({attributes[i]: {"$gte": start_of_day, "$lt": end_of_day}})
                except (ValueError, IndexError):
                    # Skip invalid date formats
                    continue
            else:
                # Add regex queries for text attributes
                search_queries.append({attributes[i]: {"$regex": search_terms[i], "$options": "i"}})

        # Combine queries with $or to match any condition
        combined_query = {"$and": search_queries}
        # Define the projection
        projection = {'_id': 0}

        # Perform the query
        return self.__mongodb_driver.find(combined_query, projection)

    
    def __print_document_metaData(self, document):
        print(f'Name: {document['name'].split('.')[0]}\nType: {document['name'].split('.')[-1]}\nNo. of Pages: {document['pages']}\nNo. of Words: {document['words']}\nNo. of Characters: {document['characters']}\nDate Uploaded: {str(document['upload date']).split('.')[0]}\nDate Modified: {str(document['modify date']).split('.')[0]}')
            
    def __most_common_words(self, words_list: list, n=5):
        word_counts = Counter(words_list)
        
        most_common = word_counts.most_common(n)
        
        print('\nMost commonly used words:\n')
        for i in range(len(most_common)):
            print(f'{i+1}) {most_common[i][0].title()} : {most_common[i][1]}')
            
    def __term_frequency(self, search_term, words):
        return round(words.count(search_term.lower())/len(words),6)
    
    def __content_preparation(self, content):
        words = self.__remove_unnecessary_words(content)
        for i in range(len(words)):
            words[i]=words[i].lower()
        return words
        
    def __remove_unnecessary_words(self,input_string):
        stop_words = set(stopwords.words('english'))
        words = re.findall(r'[A-Z][a-z]*|[^A-Z\s]+', input_string)
        filtered_words = [
        re.sub(r'[^a-zA-Z]', '', word)
        for word in words
        if word.lower() not in stop_words and re.sub(r'[^a-zA-Z]', '', word) and len(re.sub(r'[^a-zA-Z]', '', word)) > 1
    ]
        return filtered_words
        
    def extract_page_numbers_of_text(self, document: dict, search_term: str):
        pdf_data = document['file_data']
        pdf_file = fitz.open(stream=pdf_data, filetype="pdf")
        page_numbers = []

        for page_num in range(pdf_file.page_count):
            page = pdf_file.load_page(page_num)
            page_content = page.get_text("text")
            if search_term.lower() in page_content.lower():
                page_numbers.append(page_num + 1)
            
        return page_numbers

    def search_file(self, search_term: str, attribute: str):
        try:
            documents = list(self.__db_query(search_term, attribute))
            if len(documents)==0:
                print('Document not found.')
                return
            for document in documents:
                self.__print_document_metaData(document)
                self.__most_common_words(self.__remove_unnecessary_words(document['contents']))
                print('=================================================================')
        except Exception as e:
            print('Query error:',e)

    def search_contents(self, search_term):
        try:
            documents = list(self.__db_query(search_term))
            if len(documents)==0:
                print('Document not found.')
                return
            print(f'Documents that contain "{search_term}"')
            for document in documents:
                self.__print_document_metaData(document)
                prepared_content=self.__content_preparation(document['contents'])
                if ' ' in search_term:
                    print(f'Unable to calculate term frequency for multiple words')
                else:
                    print(f'Term Frequency of the term "{search_term}": {self.__term_frequency(search_term, prepared_content)} ({prepared_content.count(search_term.lower())}/{len(prepared_content)})')
                page_numbers = self.extract_page_numbers_of_text(document, search_term)
                print(f'Pages containing the search term "{search_term}": {", ".join(map(str, page_numbers))}')
                print('=================================================================')
        except Exception as e:
            print('Query error:',e)