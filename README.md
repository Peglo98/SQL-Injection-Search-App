# SQL Injection Search App

Simple Python application demonstrating SQL Injection vulnerability in search functionality.

## Project Structure

- `sql_injection_search_app.py`: Main application implementing a search over a database without input sanitization.

## Requirements

- Python 3.6+
- sqlite3 (built-in)
- Flask (if using the web interface)

## Installation

```bash
git clone https://github.com/Peglo98/SQL-Injection-Search-App.git
cd SQL-Injection-Search-App
# If the app uses Flask for a web interface:
pip install Flask
```

## Usage

Run the application:

```bash
python sql_injection_search_app.py
```

- **Web mode**: If a Flask server is started, navigate to `http://127.0.0.1:5000/` in your browser.
- **CLI mode**: Follow the command-line prompts to enter search terms.

The application constructs SQL queries by directly concatenating user input, illustrating how unsanitized inputs can lead to SQL Injection attacks.

## Project Workflow

1. **Input**: User provides a search term.
2. **Query**: The application builds a raw SQL query using the input.
3. **Execute**: The query is executed against an SQLite database.
4. **Display**: Results are returned and displayed, demonstrating potential vulnerability.
