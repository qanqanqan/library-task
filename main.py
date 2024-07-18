from library import Library

"""
Консольная программа "Библиотека"
Возможно добавление, удаление книг, изменение их статуса, отображение всех книг
и поиск книг из общего списка.
"""

def main():
    print("Library app!")
    print("Type 'options' for options list\n'exit' to exit this program")
    lib = Library()

    while True:
        choice = input("\n>>> ")

        match choice:
            case 'options':        
                print("\nHere's the list of available actions:",
                    "1 - show all books",
                    "2 - add new book",
                    "3 - delete book",
                    "4 - search for book",
                    "5 - change book status",
                    "exit - close this program", sep='\n')
            
            case '1':
                lib.show_books()

            case '2':
                print("To add a book you need to input 3 values - its title, its author and its year")
                title = input('Title: ')
                author = input('Author: ')
                year = input('Year: ')
                if title and author and year:
                    lib.add_book(title, author, year)
                    print("You've successfully added a book!")
                else:
                    print("One of the values was empty, please try again!")

            case '3':
                print("To delete a book you need to provide it's id")
                book_id = input('ID: ')
                if book_id.isdigit():
                    lib.remove_book(book_id)
                    print("You've successfully remove a book from the library!")
                else:
                    print("ID wasn't provided. Please try again!")

            case '4':
                print("To search for a book you need to input a title, an author or a year. Multiple values can be provided, in that case more choices will be shown")
                title = input('Title: ')
                author = input('Author: ')
                year = input('Year: ')
                lib.search_book(title, author, year)

            case '5':
                print("To change a book status you need to input an ID of a book and new status")
                book_id = input('ID: ')
                status = input('New status: ')

                if book_id.isdigit() and status in ['Available', 'Sold']:
                    lib.change_status(book_id, status)
                    print("You've successfully changed a book status")
                else:
                    print("One of the values was empty or incorrect, please try again!")

            case 'exit':
                break

            case _:
                print("It's not an option. Please try again!")
                

if __name__ == "__main__":
    main()
