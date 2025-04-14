# Personal Library Management System

A modern web application built with Streamlit to manage your personal book library. Track your reading progress, organize your collection, and view statistics about your reading habits.

## Features

- Add new books with details like title, author, genre, and rating
- View your complete library in a clean, organized table
- Track reading status (To Read, Reading, Completed)
- Search books by title or author
- View statistics and visualizations of your reading habits
- Modern and responsive UI

## Installation

1. Clone this repository
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the URL shown in the terminal (usually http://localhost:8501)

## Features in Detail

- **Add Book**: Add new books to your library with comprehensive details
- **View Library**: Browse your complete collection in a sortable table
- **Statistics**: View visualizations of your reading habits, including:
  - Books by genre (pie chart)
  - Books by status (bar chart)
  - Average ratings by genre
- **Search**: Quickly find books by title or author

## Data Storage

The application uses SQLite for data storage. Your library data is stored in a `library.db` file in the same directory as the application.

## Contributing

Feel free to fork this project and submit pull requests for any improvements or additional features.

## License

This project is open source and available under the MIT License. 