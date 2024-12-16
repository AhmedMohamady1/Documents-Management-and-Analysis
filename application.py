from mongopart import *
from search import *
from similarity import *

class Application:
    def __init__(self):
        self.__mongo=Mongo()
        self.__search=Search(self.__mongo.collection)
        
    def help(self):
        print("1 import file")
        print("2 delete file")
        print("3 search")
        print("4 combination search")
        print("5 compare files")
        print("0 exit")
    
    def import_file(self):
        path=input('file path: ')
        self.__mongo.Pull_File(path)  

    def delete_file(self):
        name=input('file name: ')
        self.__mongo.delete_file(name)
    
    def __search_helper():
        print("Choose the search attribute")
        print("1 name")
        print("2 modify date")
        print("3 upload date")
        print("4 contents")
        print("0 exit")
        attribute=input('attribute: ')
        match attribute:
            case '1':
                return 'name'
            case '2':
                return 'modify date'
            case '3':
                return 'upload date'
            case '4':
                return 'contents'
            case '0':
                return
            
    def search_file(self):
        attribute=self.__search_helper()
        search_term=input('search term: ')
        if attribute=='contents':
            self.__search.search_contents(search_term)
        else:
            self.__search.search_file(search_term, attribute)
    
    def combination_search(self):
        attribute1=self.__search_helper()
        attribute2=self.__search_helper()
        search_term1=input('search term: ')
        search_term2=input('search term: ')
        self.__search.search_file([search_term1,search_term2], [attribute1, attribute2])
            
            
    def similarity(self):
        print("Please insert the two files names:")
        name1 = input("File1: ")
        name2 = input("File2: ")
        texts = [list(self.__search.db_query(name1, "name"))[0]["contents"],list(self.__search.db_query(name2, "name"))[0]["contents"]]
        comparison = SimilarityGetter(texts)
        
        print("\nChoose the comparison metric:")
        print("1 Cosine similarity")
        print("2 Jaccard similarity")
        print("3 Euclidean distance (dissimilarity)")
        print("0 Back")
        choice = input("Choice: ")
        
        match choice:
            case "0":
                return
            case "1":
                return f"\nThe Cosine similarity is: {comparison.cosine_similarity()}"
            case "2":
                return f"\nThe Jaccard similarity is: {comparison.jaccard_similarity()}"
            case "3":
                return f"\nThe Euclidean distance is: {comparison.euclidean_distance()}"
            case _:
                return "\ninvalid input"
        
    def execute(self):
        self.help()
        while True:
            print("")
            command = input("command: ")
            match command:
                case "0":
                    break
                case "1":
                    self.import_file()
                case "2":
                    self.delete_file()
                case "3":
                    self.search_file()
                case "4":
                    self.combination_search()
                case "5":
                    print(self.similarity())
                case _:
                    self.help()

application=Application()
application.execute()
