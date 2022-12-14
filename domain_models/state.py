import ui.ui as ui
from domain_models.command import Command
from domain_models.actions import Actions
from domain_models.event import Event
from repository.library import Library
from domain_models.book import Book
from apis.my_sql import LibraryModel
from domain_models.pdfView import PDFFile
from fpdf import FPDF

class State:
    def __init__(self, header: str, command_list):
        self.__header = header
        self.__command_list = command_list

    def __str__(self):
        string_command_list = ''

        for command in self.__command_list:
            string_command_list += command.to_string() + '\n'

        return f'{self.__header}\n{string_command_list}'

    def to_string(self):
        string_command_list = ''

        for command in self.__command_list:
            string_command_list += command.to_string() + '\n'

        return f'{self.__header}\n{string_command_list}'

    def handle_input(self, state_manager):
        pass

class MainState(State):
    def handle_input(self, state_manager,):
        user_input = ui.get_int()
        if user_input == Actions.Exit.value:
            exit()
        elif user_input == Actions.AddBook.value:
            state_manager.change_state(States.AddBook)
        elif user_input == Actions.RemoveBook.value:
            state_manager.change_state(States.RemoveBook)
        elif user_input == Actions.Find_by_author.value:
            state_manager.change_state(States.Find_by_author)
        elif user_input == Actions.Find_by_year.value:
            state_manager.change_state(States.Find_by_year)
        elif user_input == Actions.Find_by_title.value:
            state_manager.change_state(States.Find_by_title)
        elif user_input == Actions.PrintAt.value:            
            state_manager.change_state(States.PrintAt)
        elif user_input == Actions.PrintAll.value:                       
            state_manager.change_state(States.PrintAll)   
        elif user_input == Actions.Edit.value:
            state_manager.change_state(States.Edit)
        elif user_input == Actions.Cancel.value:
            state_manager.change_state(States.Main)
        else:
            pass  # TODO incorrect input

class RemoveBookState(State):
    def handle_input(self, state_manager):
        book_list = '' 
        index = int(input('?????????????? ?????????? ?????????????????? ??????????\n'))
        if index == Actions.Cancel.value:
            state_manager.change_state(States.Main)
        else:
            library = state_manager.library.remove_at(index)  
            ui.get_sting()
            ui.clear()
            state_manager.change_state(States.Main)

class PrintAllState(State):
    def handle_input(self, state_manager):
        book_list = ''
        i = 0
        book_list = state_manager.library.get_all_books()
        for book in book_list:
            i += 1
            print(f'{i} - ', book)
        pdf=FPDF()
        pdf.add_page()
        pdf.add_font('DejaVu', style="", fname="domain_models/font/DejaVuSansCondensed.ttf", uni=True)
        pdf.set_font('DejaVu', '', 14)
        for book in book_list:
            text=str(book)
            text=text.replace('(', ' ')
            text=text.replace(')', ' ')
            pdf.cell(20,10,txt=text,ln=1)
        pdf.output('pdf/All_books.pdf')
        print('PDF-???????? ?????????????? ????????????')
        ui.get_sting()        
        ui.clear()
        state_manager.change_state(States.Main)       
        
class AddBookState(State):
    def handle_input(self, state_manager):
        title = input("?????????????? ???????????????? ??????????\n") 
        if title == str(Actions.Cancel.value):
            state_manager.change_state(States.Main)
        else:
            year = int(input("?????????????? ?????? ????????\n"))
            if year == Actions.Cancel.value:
                state_manager.change_state(States.Main)
            else:
                author = input("?????????????? ???????????? ??????????\n") 
                if author == str(Actions.Cancel.value):
                    state_manager.change_state(States.Main)
                else:
                    book = Book(title, year, author)
                    library = state_manager.library.add(book)
                    ui.get_sting()
                    ui.clear()
                    state_manager.change_state(States.Main)
        
class PrintAtState(State):
    def handle_input(self, state_manager):
        book_list = ''
        index = int(input('?????????????? ?????????? ???????????????????????? ??????????\n'))
        if index == Actions.Cancel.value:
            state_manager.change_state(States.Main)
        else:
            book_list = state_manager.library.get_at(index)                         
            ui.draw_ui(book_list)
            pdf=FPDF()
            pdf.add_page()
            pdf.add_font('DejaVu', style="", fname="domain_models/font/DejaVuSansCondensed.ttf", uni=True)
            pdf.set_font('DejaVu', '', 14)
            text=str(book_list)
            pdf.cell(20,10,txt=text,ln=1)  
            pdf.output('pdf/One_book.pdf')
            print('PDF-???????? ?????????????? ????????????')
            ui.get_sting()
            ui.clear()
            state_manager.change_state(States.Main)
        
class Find_by_authorState(State):
    def handle_input(self, state_manager):
        book_list = ''
        author = input('?????????????? ???????????? ??????????\n')
        if author == str(Actions.Cancel.value):
            state_manager.change_state(States.Main)
        else:
            book_list = state_manager.library.find_by_author(author)  
            for book in book_list:              
                ui.draw_ui(book)
            pdf=FPDF()
            pdf.add_page()
            pdf.add_font('DejaVu', style="", fname="domain_models/font/DejaVuSansCondensed.ttf", uni=True)
            pdf.set_font('DejaVu', '', 14)
            for book in book_list:
                text=str(book)
                text=text.replace('(', ' ')
                text=text.replace(')', ' ')
                pdf.cell(20,10,txt=text,ln=1)
            pdf.output('pdf/Books_By_Author.pdf')
            print('PDF-???????? ?????????????? ????????????')
            ui.get_sting()
            ui.clear()
            state_manager.change_state(States.Main)
        
class Find_by_titleState(State):
    def handle_input(self, state_manager):
        book_list = ''
        title = input('?????????????? ???????????????? ??????????\n')
        if title == str(Actions.Cancel.value):
            state_manager.change_state(States.Main)
        else:
            book_list = state_manager.library.find_by_title(title)  
            for book in book_list:              
                ui.draw_ui(book)
            ui.get_sting()
            ui.clear()
            state_manager.change_state(States.Main)
        
class Find_by_yearState(State):
    def handle_input(self, state_manager):
        book_list = ''
        year = input('?????????????? ?????? ??????????\n')
        if year == Actions.Cancel.value:
            state_manager.change_state(States.Main)
        else:
            book_list = state_manager.library.find_by_year(year)               
            for book in book_list:
                ui.draw_ui(book)
            ui.get_sting()
            ui.clear()
            state_manager.change_state(States.Main)
        
class EditState(State):
    def handle_input(self, state_manager):
        index = int(input('?????????????? ?????????? ???????????????????? ??????????\n'))
        if index == Actions.Cancel.value:
            state_manager.change_state(States.Main)
        else:
            title = input("?????????????? ?????????? ????????????????\n") 
            if title == str(Actions.Cancel.value):
                state_manager.change_state(States.Main)
            else:
                year = int(input("?????????????? ?????????? ??????\n")) 
                if year == Actions.Cancel.value:
                    state_manager.change_state(States.Main)
                else:
                    author = input("?????????????? ???????????? ????????????\n") 
                    if author == str(Actions.Cancel.value):
                        state_manager.change_state(States.Main)
                    else:
                        book = Book(title, year, author)
                        library = state_manager.library.update_at(index, book)
                        ui.get_sting()
                        ui.clear()
                        state_manager.change_state(States.Main)

class StateManager:
    def __init__(self, library: Library):
        self.state_changed = Event()
        self.__current_state = States.Main
        self.library = library
        self.is_work = True

    @property
    def current_state(self):
        return self.__current_state

    def change_state(self, state: State):
        self.__current_state = state
        ui.clear()
        string_state = self.__current_state.to_string() % self.library.count()
        self.state_changed.invoke(string_state)

class States:
    Main = MainState(f'???????????? ?? ???????????????????? %s ????????.', [        
        Command(Actions.AddBook, "???????????????????? ??????????"),
        Command(Actions.RemoveBook, "???????????????? ??????????"),        
        Command(Actions.PrintAt, "???????????? ?????????????????? ???????????????????? ?? ??????????"),
        Command(Actions.PrintAll, "???????????? ???????? ????????"),
        Command(Actions.Find_by_author, "???????????? ?????????? ???? ????????????"),
        Command(Actions.Find_by_year, "???????????? ?????????? ???? ????????"),
        Command(Actions.Find_by_title, "???????????? ?????????? ???? ????????????????"),
        Command(Actions.Edit, "???????????????????????????? ??????????"),
        Command(Actions.Exit, "????????????")
    ])

    AddBook = AddBookState(f'???????????? ?? ???????????????????? %s ????????.', [
        Command(Actions.Cancel, "????????????")
    ])

    RemoveBook = RemoveBookState(f'???????????? ?? ???????????????????? %s ????????.', [
        Command(Actions.Cancel, "????????????")
    ])

    PrintAll = PrintAllState(f'???????????? ?? ???????????????????? %s ????????.', [
        Command(Actions.Cancel, "????????????")
    ])
    
    PrintAt = PrintAtState(f'???????????? ?? ???????????????????? %s ????????.', [
        Command(Actions.Cancel, "????????????")
    ])
    
    Find_by_author = Find_by_authorState(f'???????????? ?? ???????????????????? %s ????????.', [
        Command(Actions.Cancel, "????????????")
    ])
    
    Find_by_year = Find_by_yearState(f'???????????? ?? ???????????????????? %s ????????.', [
        Command(Actions.Cancel, "????????????")
    ])
    
    Find_by_title = Find_by_titleState(f'???????????? ?? ???????????????????? %s ????????.', [
        Command(Actions.Cancel, "????????????")
    ])
    
    PrintAll = PrintAllState(f'???????????? ?? ???????????????????? %s ????????.', [
        Command(Actions.Return, "???????????? ?? ?????????????? ????????")
    ])
    
    Edit = EditState(f'???????????? ?? ???????????????????? %s ????????.', [
        Command(Actions.Cancel, "????????????")
    ])