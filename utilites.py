def book_to_dict(book):
    row = {"id": book.id, "title": book.title, "genre":book.genre.name, "author": book.author, "added_by": book.user.name, "user_id": book.user_id, "genre_id": book.genre_id}
    return row

# def get_books(title=None, author=None, genre=None):
#     session = Session()
#     filters = []
    
#     if title:
#         filters.append(Book.title == title)
#     if author:
#         filters.append(Book.author == author)
#     if genre:
#         filters.append(Book.genre == genre)
    
#     if filters:
#         books = session.execute(db.select(Book).where(and_(*filters))).scalars().all()
#     else:
#         books = session.execute(db.select(Book)).scalars().all()
    
#     return books