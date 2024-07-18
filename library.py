import json


class Library:
    """
    Класс Library представляет интерфейс библиотеки для работы с книгами

    Имплементированы базовые операции, касаемые работы библиотеки:
    - добавление и удаление книг,
    - отображение книг и их текущего статуса,
    - изменение статуса книги,
    - поиск книг по нескольким параметрам - названию, автору и году выхода

    
    Атрибуты
    ----------
    Приватные атрибуты

    __books : dict[str, dict[str, str | int]]
        хэш-таблица с указателем в виде ID книги на словарь с ее данными - 
        названием, автором и годом, 
        представленными в виде строк и целого числа

    __book_id : str
        глобальный счетчик, используемый для указания ID книги при добавлении

    __authors : dict[str, list[str]]
        объект словаря с перечислением всех известных библиотеке авторов книг
        со списком ID их книг.
        необходим для лучшего поиска по авторам, "индексации"

    __titles : dict[str, list[str]]
        объект словаря с перечислением всех известных библиотеке названий книг
        со списком ID этих книг.
        необходим для лучшего поиска по названиям, "индексации"

    __years : dict[str, list[str]]
        объект словаря с перечислением всех годов выпусков книг со списком ID 
        этих книг.
        необходим для лучшего поиска по годам, "индексации"

    __mainfile : str
        стандартное название json-файла для хранения общих данных о книгах

    __aidxfile : str
        стандартное название json-файла для хранения проиндексированных значений
        книг по авторам

    __tidxfile : str
        стандартное название json-файла для хранения проиндексированных значений
        книг по названиям

    __yidxfile : str
        стандартное название json-файла для хранения проиндексированных значений
        книг по годам

    ------
    Методы
    ------
    Публичные методы
    
    add_book(title : str, author : str, year : str) -> None
        Добавляет в таблицу книг очередное значение.
        После обновляет данные в бэкап-файлах, инкрементирует глобальный 
        счетчик индекса книг
    
    remove_book(book_id : str) -> None
        Выполняет операцию удаления книги по передаваемому значению ID.
        Если книга с таким ID не найдена, удаление не будет произведено.
        Удаление происходит также в индексируемых таблицах.
        После происходит обновление информации бэкап-файлов.

    search_book(title : str (default ''), author : str (default ''), year : str(default None)) -> None
        Воспроизводит поиск книги по одному и более(до трех) параметрам - названию, году и автору.
        Результат поиска выводится на экран по различных категориям поиска - отдельно
        по названию, отдельно по году и отдельно по автору.
        Если результаты поиска пусты, то выводится соответствующее сообщение об этом.

    change_status(book_id : str, status : str) -> None
        Производит изменение статуса книги по ее ID на новое значение.
        Если книга с таким ID не найдена, изменение статуса не будет произведено.
    
    show_books() -> None
        Отображает все имеющиеся в библиотеке книги и их полные данные.
        Если книги отсутствуют, то выводится сообщение об их отсутствии.
    
    -----
    Приватные методы

    __files_init() -> None
        Открытие бэкап-файлов и сохранение данных из них индексируемых данных и общих данных
        о книгах в библиотеке.
        Также происходит переопределение глобального счетчика ID книг для его корректной работы.

    __write_index_authors() -> None
        Запись значений таблицы индексируемых по авторам значений ID книг в соответствующий файл

    __write_index_titles() -> None
        Запись значений таблицы индексируемых по названиям значений ID книг в соответствующий файл
    
    __write_index_years() -> None
        Запись значений таблицы индексируемых по годам значений ID книг в соответствующий файл

    __index_authors(author : str, book_id : str) -> None
        Индексация значения книги по автору - добавление нового ID книги соотвутствующему автору 
        в таблицу индексов.
        Также происходит сохранение значений в соотвутствующий файл.

    __index_titles(title : str, book_id : str) -> None
        Индексация значения книги по названию - добавление нового ID книги соотвутствующему названию 
        в таблицу индексов.
        Также происходит сохранение значений в соотвутствующий файл.
        
    __index_years(year : str, book_id : str) -> None
        Индексация значения книги по годам - добавление нового ID книги соотвутствующему году 
        в таблицу индексов.
        Также происходит сохранение значений в соотвутствующий файл.

    __show_book(book_id : str) -> None
        Отображение информации о книге по переданному ID.
    """
    def __init__(self) -> None:
        self.__books = {}
        self.__book_id = "0"

        self.__authors = {}
        self.__titles = {}
        self.__years = {}

        self.__mainfile = 'mainfile.json'
        self.__aidxfile = 'authors.json'
        self.__tidxfile = 'titles.json'
        self.__yidxfile = 'years.json'

        # Если хотя бы один из файлов отсутствует, то чтение данных не будет выполнено
        try:
            self.__files_init()
        except FileNotFoundError:
            print("You are working with an empty library")

    # PRIVATE METHODS
    def __files_init(self) -> None:
        with open(self.__mainfile, 'r', encoding='UTF-8') as file:
            self.__books = json.loads(file.read())
        
        with open(self.__aidxfile, 'r', encoding='UTF-8') as file:
            self.__authors = json.loads(file.read())

        with open(self.__tidxfile, 'r', encoding='UTF-8') as file:
            self.__titles = json.loads(file.read())

        with open(self.__yidxfile, 'r', encoding='UTF-8') as file:
            self.__years = json.loads(file.read())
        
        self.__book_id = str(max(map(int, self.__books.keys())) + 1)

    def __write_index_authors(self) -> None:
        with open(self.__aidxfile, 'w', encoding='UTF-8') as file:
            file.write(json.dumps(self.__authors))
    
    def __write_index_titles(self) -> None:
        with open(self.__tidxfile, 'w', encoding='UTF-8') as file:
            file.write(json.dumps(self.__titles))

    def __write_index_years(self) -> None:
        with open(self.__yidxfile, 'w', encoding='UTF-8') as file:
            file.write(json.dumps(self.__years))

    def __write_mainfile(self) -> None:
        with open(self.__mainfile, 'w', encoding='UTF-8') as file:
            file.write(json.dumps(self.__books))

    def __index_authors(self, author: str, book_id: str) -> None:
        if not author in self.__authors:
            self.__authors[author] = [book_id]
        else:
            self.__authors[author].append(book_id)

        self.__write_index_authors()

    def __index_titles(self, title: str, book_id: str) -> None:
        if not title in self.__titles:
            self.__titles[title] = [book_id]
        else:
            self.__titles[title].append(book_id)

        self.__write_index_titles()

    def __index_years(self, year: str, book_id: str) -> None:
        if not year in self.__years:
            self.__years[year] = [book_id]
        else:
            self.__years[year].append(book_id)
        
        self.__write_index_years()

    def __show_book(self, book_id: str) -> None:
        book_info = self.__books[book_id]
        print(
            f'id - {book_id}',
            f'title - {book_info["title"]}',
            f'author - {book_info["author"]}',
            f'year - {book_info["year"]}',
            f'status - {book_info["status"]}',
            sep='\n',
        )
    
    # PUBLIC METHODS
    def add_book(self, title: str, author: str, year: str) -> None:
        self.__books.update({
            self.__book_id: {
            'title': title,
            'author': author,
            'year': year,
            'status': 'Available',
            },
        })

        self.__index_authors(author, self.__book_id)
        self.__index_titles(title, self.__book_id)
        self.__index_years(year, self.__book_id)

        self.__write_mainfile()

        self.__book_id = str(int(self.__book_id) + 1)
    
    def remove_book(self, book_id: str) -> None:
        if not book_id in self.__books.keys():
            print("Can't find a book with provided ID")
            return
        
        book_info = self.__books[book_id]
        
        self.__titles[book_info['title']].remove(book_id)
        self.__authors[book_info['author']].remove(book_id)
        self.__years[book_info['year']].remove(book_id)

        self.__books.pop(book_id)

        self.__write_index_authors()
        self.__write_index_titles()
        self.__write_index_years()
        self.__write_mainfile()
    
    def search_book(self, title:str = '', author: str = '', year: str|None = None) -> None:
        search_result = {
            'by_title': {},
            'by_author': {},
            'by_year': {},
        }
        if title:
            search_result['by_title'] = {
                'title': title,
                'books_ids': self.__titles[title],
            }
            books_ids = search_result['by_title'].get('books_ids')
            
            print('======\nBy title:' if books_ids else "Can't find anything by title")
            for book_id in books_ids:
                print('-'*20)
                self.__show_book(book_id)

        if author:
            search_result['by_author'] = {
                'author': author,
                'books_ids': self.__authors[author],
            }
            books_ids = search_result['by_author'].get('books_ids')

            print('======\nBy author:' if books_ids else "Can't find anything by author")
            for book_id in books_ids:
                print('-'*20)
                self.__show_book(book_id)

        if year:
            search_result['by_year'] = {
                'year': year,
                'books_ids': self.__years[year],
            }
            books_ids = search_result['by_year'].get('books_ids')

            print('======\nBy year:' if books_ids else "Can't find anything by year")
            for book_id in books_ids:
                print('-'*20)
                self.__show_book(book_id)

    def change_status(self, book_id: str, status: str) -> None:
        if not book_id in self.__books.keys():
            print("Can't find book with provided ID")
            return
        
        self.__books[book_id]['status'] = status

        self.__write_mainfile()

    def show_books(self) -> None:
        print("Books list" if self.__books else "Library is empty")
        for book_id in self.__books:
            print('-'*20)
            self.__show_book(book_id)
