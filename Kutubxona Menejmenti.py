import json
from datetime import datetime, timedelta
from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.metrics.pairwise import cosine_similarity

class Book:
    def __init__(self, title, author, genre, description):
        self.title = title
        self.author = author
        self.genre = genre
        self.description = description

        self.available = True
        self.rent_count = 0

class User:
    def __init__(self, name):
        self.name = name
        self.borrowed_books = []

    def borrow_book(self, book, days=7):
        if book.available:
            due_date = datetime.now() + timedelta(days= days)

            self.borrowed_books.append({
                "book": book,
                "due_date": due_date
            })

            book.available = False
            book.rent_count += 1
            print(f"{book.title} borrowed successfully")

        else:
            print("Book is not available")

    
    def return_book(self, book):
        for item in self.borrowed_books:
            if item["book"] == book:
                self.borrowed_books.remove(item)

                book.available = True
                print(f"{book.title} returned successfully")
                return 
        print("Book not fount")

    def extend_due_date(self, book, extra_days):
        for item in self.borrowed_books:
            if item["book"] == book:
                item["due_date"] += timedelta(days=extra_days)
                print(f"Due date extended by {extra_days} days")
                return  
            
class Admin(User):
    def add_book(self, library, book):
        library.books.append(book)

        print(f"{book.title} added to library")

    def remove_user(self, library, user):
        if user in library.users:
            library.users.remove(user)
            print(f"{user.name} removed")


class Library:
    def __init__(self):
        self.books = []
        self.users = []

    def add_user(self, user):
        self.users.append(user)

    def search_book(self, keyword):
        result = []

        for book in self.books:
            if keyword.lower() in book.title.lower():
                result.append(book)

        return result
    
    def list_books(self):
        for book in self.books:
            print({
                "title": book.title,
                "author": book.author,
                "genre": book.genre,
                "available": book.available,
                "rent_count": book.rent_count 
            })

    def save_books(self):
        data = []

        for book in self.books:
            data.append({
                "title": book.title,
                "author": book.author,
                "genre": book.genre,
                "description": book.description,
                "available": book.available,
                "rent_count": book.rent_count
            })

        with open("books.json", "w") as file:
            json.dump(data, file, indent=4)

        print("Books saved")

    
    def load_books(self):
        with open("books.json", "r") as file:
            data = json.load(file)

        for item in data:
            book = Book(
                item["title"],
                item["author"],
                item["genre"],
                item["description"]
            )

            book.available = item["available"]
            book.rent_count = item["rent_count"]

            self.books.append(book)

            print("Books loaded")

    
    def save_users(self):
        data = []

        for user in self.users:
            data.append({
                "name": user.name
            })
        
        with open("users.json", "r") as file:
            json.dump(data, file, indent=4)

            print("Users saved")


    
    def load_users(self):
        with open("users.json", "r") as file:
            data = json.load(file)

        for item in data:
            user = User(item["name"])

            self.users.append(user)

            print("Users loaded")


    def recommend_books(self, book_title):
        description = []
        titles = []

        for book in self.books:
            description.append(book.description)
            titles.append(book.title)

        vectorizer = TfidfVectorizer()
        matrix = vectorizer.fit_transform(description)
        similarity = cosine_similarity(matrix)
        index= titles.index(book_title)
        similarity_scores = list(enumerate(similarity[index]))
       #[1.0, 0.9, 0.1]   -   # [(0,1.0), (1,0.9), (2,0.1)]
        similarity_scores = sorted(
            similarity_scores,
            key= lambda x: x[1],
            reverse=True
        )

        print("\nRecommended books:")

        for i in similarity_scores[1:4]: #3 ta recommendation
            print(titles[i[0]])

    
    def check_overdue_books(self):
        today = datetime.now()
        for user in self.users:
            for item in user.borrowed_books:
                if today > item["due_date"]:
                    print(
                        f"Warning: {user.name} did not return {item["book"].title} "
                        )
                    
    
    def most_read_book(self):
        most_read = max(self.books, key=lambda book: book.rent_count)

        print("Most read:", most_read.title)

    def least_rented_book(self):
        least = min(self.books, key=lambda book: book.rent_count)

        print("Least rented:", least.title)


class LibraryCLI:
    def __init__(self):
        self.library = Library()

    def run(self):
        while True:
            print("\n1. Add Book")
            print("2. Add User")
            print("3. List Books")
            print("4. Search Book")
            print("5. Recommend Books")
            print("6. Save Books")
            print("7. Load Books")
            print("8. Exit")

            choice = input("Choice:")

            if choice == "1":
                title = input("Title:")
                author = input("Author:")
                genre = input("Genre:")
                description = input("Description:")

                book = Book(title, author, genre, description)

                self.library.books.append(book)

            elif choice == "2":
                name = input("User name: ")
                user = User(name)

                self.library.users.append(user)

            elif choice == "3":
                self.library.list_books()

            elif choice == "4":
                keyword = input("Keyword: ")

                books = self.library.search_book(keyword)

                for book in books:
                    print(book.title)

            elif choice == "5":
                title = input("Book title: ")
                self.library.recommend_books(title)

            elif choice == "6":
                self.library.save_books()

            elif choice == "7":
                self.library.load_books()

            elif choice == "8":
                break

cli = LibraryCLI()
cli.run()