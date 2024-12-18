from mongopart import *
from search import *
from similarity import *

class Application:
    def __init__(self):
        self.__mongo = Mongo()
        self.__search = Search(self.__mongo.collection)
        
    def help(self):
        print("1 import file")
        print("2 delete file")
        print("3 search")
        print("4 combination search")
        print("5 compare files")
        print("0 exit")
    
    def import_file(self):
        try:
            path = input('file path: ')
            self.__mongo.Pull_File(path)
        except Exception as e:
            print(f"Error importing file: {e}")

    def delete_file(self):
        try:
            name = input('file name: ')
            self.__mongo.delete_file(name)
        except Exception as e:
            print(f"Error deleting file: {e}")
    
    def __search_helper(self):
        print("choose the search attribute")
        print("1 name")
        print("2 modify date (in yyyy-mm-dd)")
        print("3 upload date (in yyyy-mm-dd)")
        print("4 contents")

        while True:
            attribute = input('attribute: ')
            match attribute:
                case '1':
                    return 'name'
                case '2':
                    return 'modify date'
                case '3':
                    return 'upload date'
                case '4':
                    return 'contents'
                case _:
                    print('invalid input')
            
    def search_file(self):
        attribute = self.__search_helper()
        search_term = input('search term: ')
        if attribute == 'contents':
            self.__search.search_contents(search_term)
        else:
            self.__search.search_file(search_term, attribute)

    def combination_search(self):
        try:
            n = int(input('number of conditions: '))
            attributes = []
            search_terms = []
            for i in range(n):
                attributes.append(self.__search_helper())
                search_terms.append(input('search term: '))
            print('')
            self.__search.search_file(search_terms, attributes)
            
        except Exception as e:
            print(f"Error during combination search: {e}")
        
    def similarity(self):
        print("Please insert the two files names:")
        name1 = input("File1: ")
        name2 = input("File2: ")
        try:
            texts = [
                list(self.__search.db_query(name1, "name"))[0]["contents"],
                list(self.__search.db_query(name2, "name"))[0]["contents"]
            ]
        except IndexError:
            print("One or both files were not found.")
            return
        
        comparison = SimilarityGetter(texts)
        
        print("\nChoose the comparison metric:")
        print("1 Cosine similarity")
        print("2 Jaccard similarity")
        print("3 Euclidean distance (dissimilarity)")
        print("0 Back")
        print('')
        while True:
            choice = input("Choice: ")
            match choice:
                case "0":
                    print("Exiting...")
                    break
                case "1":
                    print(f"The Cosine similarity is: {comparison.cosine_similarity()}")
                    break
                case "2":
                    print(f"The Jaccard similarity is: {comparison.jaccard_similarity()}")
                    break
                case "3":
                    print(f"The Euclidean distance is: {comparison.euclidean_distance()}")
                    break
                case _:
                    print("Invalid input")

    def execute(self):
        while True:
            self.help()
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
                    self.similarity()
                case _:
                    print("Invalid command. Please try again.")
            print("")

if __name__=='__main__':
    application = Application()
    application.execute()