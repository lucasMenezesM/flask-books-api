def book_to_dict(book):
    row = {"id": book.id, "title": book.title, "genre":book.genre.name, "author": book.author, "added_by": book.user.name, "user_id": book.user_id, "genre_id": book.genre_id, "added_date": book.added_date, "description": book.description}
    return row

def user_to_dict(user):
    books = [book_to_dict(book) for book in user.books]
    row = {"id": user.id, "name": user.name, "books": books, "email": user.email, "register_date": user.register_date}
    return row

def genre_to_dic(genre):
    books = [book_to_dict(book) for book in genre.books]
    row = {"id": genre.id, "name": genre.name, "books": books}
    return row