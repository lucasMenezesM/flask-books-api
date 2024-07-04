from sqlalchemy import Integer, String, Text
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, DateTime
from datetime import datetime, UTC
from flask_login import UserMixin

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    email: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    register_date: Mapped[str] = mapped_column(DateTime, default=datetime.now(UTC))

    books = db.relationship("Book", back_populates="user")
    

class Book(db.Model):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    added_date: Mapped[str] = mapped_column(DateTime, default=datetime.now(UTC))
    description: Mapped[str] = mapped_column(Text)

    genre_id: Mapped[int] = mapped_column(Integer, db.ForeignKey('genres.id'), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, db.ForeignKey('users.id'), nullable=False)

    user = relationship("User", back_populates="books")
    genre = relationship("Genre", back_populates="books")

    def columns_to_dict(self):
        dict_ = {}
        for key in self.__mapper__.c.keys():
            dict_[key] = getattr(self, key)
        return dict_
    
    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Genre(db.Model):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)

    books = db.relationship("Book", back_populates="genre")
    
