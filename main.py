import peewee
from repository.library import Library
from app import App

if __name__ == '__main__':
    App.run()
    try:

        library = Library()
        library.connect()
        print(library.count())
        print(library.get_at(1))
        print(library.get_all_books())
        library.close()

    except peewee.InternalError as px:
        print(str(px))
