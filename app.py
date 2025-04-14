import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import sqlite3
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Initialize SQLite database
Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    genre = Column(String)
    rating = Column(Float)
    status = Column(String)  # 'To Read', 'Reading', 'Completed'
    date_added = Column(DateTime, default=datetime.now)
    date_completed = Column(DateTime, nullable=True)

# Create database and tables
engine = create_engine('sqlite:///library.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Set page config
st.set_page_config(
    page_title="Personal Library",
    page_icon="📚",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
    }
    .stTextInput>div>div>input {
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
st.sidebar.title("📚 Personal Library")
menu = st.sidebar.selectbox(
    "Menu",
    ["Add Book", "View Library", "Statistics", "Search"]
)

# Main content
st.title("📚 Personal Library Management")

if menu == "Add Book":
    st.header("Add New Book")
    with st.form("add_book_form"):
        title = st.text_input("Title")
        author = st.text_input("Author")
        genre = st.selectbox("Genre", ["Fiction", "Non-Fiction", "Science Fiction", "Fantasy", "Mystery", "Biography", "Other"])
        rating = st.slider("Rating", 1.0, 5.0, 3.0, 0.5)
        status = st.selectbox("Status", ["To Read", "Reading", "Completed"])
        
        submitted = st.form_submit_button("Add Book")
        if submitted:
            if title and author:
                new_book = Book(
                    title=title,
                    author=author,
                    genre=genre,
                    rating=rating,
                    status=status,
                    date_added=datetime.now()
                )
                session.add(new_book)
                session.commit()
                st.success("Book added successfully!")
            else:
                st.error("Please fill in all required fields.")

elif menu == "View Library":
    st.header("Your Library")
    books = session.query(Book).all()
    
    if books:
        df = pd.DataFrame([{
            'Title': book.title,
            'Author': book.author,
            'Genre': book.genre,
            'Rating': book.rating,
            'Status': book.status,
            'Date Added': book.date_added.strftime('%Y-%m-%d')
        } for book in books])
        
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No books in your library yet. Add some books to get started!")

elif menu == "Statistics":
    st.header("Library Statistics")
    books = session.query(Book).all()
    
    if books:
        df = pd.DataFrame([{
            'Genre': book.genre,
            'Status': book.status,
            'Rating': book.rating
        } for book in books])
        
        col1, col2 = st.columns(2)
        
        with col1:
            genre_counts = df['Genre'].value_counts()
            fig_genre = px.pie(
                values=genre_counts.values,
                names=genre_counts.index,
                title="Books by Genre"
            )
            st.plotly_chart(fig_genre, use_container_width=True)
        
        with col2:
            status_counts = df['Status'].value_counts()
            fig_status = px.bar(
                x=status_counts.index,
                y=status_counts.values,
                title="Books by Status"
            )
            st.plotly_chart(fig_status, use_container_width=True)
        
        st.subheader("Average Rating by Genre")
        avg_ratings = df.groupby('Genre')['Rating'].mean().reset_index()
        fig_ratings = px.bar(
            avg_ratings,
            x='Genre',
            y='Rating',
            title="Average Rating by Genre"
        )
        st.plotly_chart(fig_ratings, use_container_width=True)
    else:
        st.info("No statistics available. Add some books to see your library statistics!")

elif menu == "Search":
    st.header("Search Books")
    search_term = st.text_input("Search by title or author")
    
    if search_term:
        books = session.query(Book).filter(
            (Book.title.ilike(f"%{search_term}%")) | 
            (Book.author.ilike(f"%{search_term}%"))
        ).all()
        
        if books:
            df = pd.DataFrame([{
                'Title': book.title,
                'Author': book.author,
                'Genre': book.genre,
                'Rating': book.rating,
                'Status': book.status
            } for book in books])
            
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No books found matching your search.") 