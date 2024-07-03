def book_to_dict(book):
    row = {"id": book.id, "title": book.title, "genre":book.genre.name, "author": book.author, "added_by": book.user.name, "user_id": book.user_id, "genre_id": book.genre_id}
    return row

def user_to_dict(user):
    books = [book_to_dict(book) for book in user.books]
    row = {"id": user.id, "name": user.name, "books": books, "email": user.email}
    return row