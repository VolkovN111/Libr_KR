from enum import Enum

class Actions(Enum):    
    AddBook = 1
    RemoveBook = 2    
    PrintAt = 3
    PrintAll = 4
    Find_by_author = 5
    Find_by_year = 6
    Find_by_title = 7
    Edit = 8
    Exit = 9
    Cancel = 0
    Return = "Что-нибудь"
