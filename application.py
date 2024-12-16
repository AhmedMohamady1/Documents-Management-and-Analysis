from mongopart import *
from search import *
from similarity import *

class CourseRecordsApplication:
        
    def add_course(self):
        name=input('course: ')
        grade=int(input('grade: '))
        credits=int(input('credits: '))
        self.__courserecords.add_course(name,grade,credits)

    def get_course(self):
        name=input('course: ')
        self.__courserecords.get_course(name)
    
    def get_statistics(self):
        self.__courserecords.print_statistics()
        
    def execute(self):
        self.help()
        while True:
            print("")
            command = input("command: ")
            if command == "0":
                break
            elif command == "1":
                self.add_course()
            elif command == "2":
                self.get_course()
            elif command == "3":
                self.get_statistics()
            else:
                self.help()

application = CourseRecordsApplication()
application.execute()

class Application:
    def __init__(self):
        self.__search=Search()
        self.__mongo=Mongo()
        self.__similarity=SimilarityGetter()
        
    def help(self):
        print("1 import file")
        print("2 delete file")
        print("3 search file")
        print("4 search contents")
        print("5 compare files")
        print("0 exit")
    
    def import_file(self):
        path=input('file path: ')
        self.__mongo.Pull_File(path)  

    def delete_file(self):
        name=input('file name: ')
        self.__mongo.delete_file(name)
    
    def search_file(self):
        search_term=input('search term: ')
        attribute=input('attribute: ')
        self.__search.search_file(search_term,attribute)
    
    def search_contents(self):
        search_term=input('search term: ')
        self.__search.search_contents(search_term)
    
    def similarity(self):
        print("1 ")
        print("2 delete file")
        print("3 search file")
        print("4 search contents")
        print("5 compare files")
        print("0 exit")
        
    def execute(self):
        self.help()
        while True:
            print("")
            command = input("command: ")
            if command == "0":
                break
            elif command == "1":
                self.import_file()
            elif command == "2":
                self.delete_file()
            elif command == "3":
                self.search_file()
            elif command == "4":
                self.search_contents
            elif command == "5":
                self.get_statistics()
            else:
                self.help()