from peewee import MySQLDatabase
from apis.my_sql import LibraryModel
from domain_models.book import Book

class Library:
    def __init__(self, data_base=MySQLDatabase('libr', user='zxc', password='yDPq[sK6PzvsOdci',
                                               host='localhost', port=3306)):
        self.__data_base = data_base
        self.__library_model = LibraryModel()
        self.__library_model._meta.database = self.__data_base

    @staticmethod
    def __get_book(book):
        return Book(
            author=book.author,
            title=book.title,
            year=book.year
        )

    @staticmethod
    def __get_books(books):
        book_list = []
        for book in books:
            book_list.append(
                (
                    book.id,
                    Book(
                        author=book.author,
                        title=book.title,
                        year=book.year
                    )
                )
            )
        return book_list

    def remove_at(self, index: int):
        self.__library_model.get_by_id(index).delete_instance()        
            
    def get_at(self, index: int):
        return self.__get_book(self.__library_model.get_by_id(index))

    def update_at(self, index, book: Book):
        instance: LibraryModel
        instance = self.__library_model.get_by_id(index)
        instance.year = book.year
        instance.author = book.author
        instance.title = book.title
        instance.save()

    def connect(self):
        self.__data_base.connect()

    def close(self):
        self.__data_base.close()

    def add(self, book: Book):
        self.__library_model.create(
            author=book.author,
            year=book.year,
            title=book.title
        )

    def find_by_author(self, author):
        query = self.__library_model.select().where(LibraryModel.author.contains(author))
        return self.__get_books(query)
    
    def find_by_title(self, title):
        query = self.__library_model.select().where(LibraryModel.title.contains(title))
        return self.__get_books(query)

    def find_by_year(self, year):        
        query = self.__library_model.select().where(LibraryModel.year == year)
        return self.__get_books(query)        

    def count(self):
        return self.__library_model.select().count()        

    def get_all_books(self):
        query = self.__library_model.select()
        return self.__get_books(query)
