from flask import Flask, request, render_template_string
import mysql.connector

app = Flask(__name__)

TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Wyszukiwarka postów</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Roboto', sans-serif;
            line-height: 1.6;
            background-color: #f5f5f5;
            color: #333;
            padding: 2rem;
        }
        
        .container {
            max-width: 1000px;
            margin: 0 auto;
            background-color: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        h1 {
            color: #2c3e50;
            margin-bottom: 1.5rem;
            text-align: center;
            font-size: 2.5rem;
        }
        
        .search-form {
            margin-bottom: 2rem;
            text-align: center;
        }
        
        .search-form input[type="text"] {
            width: 60%;
            padding: 12px;
            font-size: 16px;
            border: 2px solid #ddd;
            border-radius: 25px;
            margin-right: 10px;
            outline: none;
            transition: border-color 0.3s ease;
        }
        
        .search-form input[type="text"]:focus {
            border-color: #3498db;
        }
        
        .search-form button {
            padding: 12px 24px;
            font-size: 16px;
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        
        .search-form button:hover {
            background-color: #2980b9;
        }
        
        .results-info {
            margin: 1rem 0;
            color: #666;
            font-size: 1.1rem;
            text-align: center;
        }
        
        .results-container {
            display: grid;
            gap: 1.5rem;
            margin-top: 2rem;
        }
        
        .post-card {
            background: white;
            padding: 1.5rem;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            transition: transform 0.2s ease;
        }
        
        .post-card:hover {
            transform: translateY(-3px);
        }
        
        .post-title {
            color: #2c3e50;
            font-size: 1.25rem;
            margin-bottom: 0.5rem;
            font-weight: 500;
        }
        
        .post-content {
            color: #666;
            font-size: 1rem;
            line-height: 1.6;
        }
        
        .highlight {
            background-color: #fff3cd;
            padding: 0 3px;
            border-radius: 3px;
        }
        
        .no-results {
            text-align: center;
            color: #666;
            font-style: italic;
            margin-top: 2rem;
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 1rem;
            }
            
            .search-form input[type="text"] {
                width: 100%;
                margin-bottom: 1rem;
            }
            
            .search-form button {
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📚 Wyszukiwarka postów</h1>
        
        <div class="search-form">
            <form method="GET">
                <input type="text" 
                       name="keyword" 
                       placeholder="Wpisz słowo kluczowe..." 
                       value="{{ keyword }}"
                       autocomplete="off">
                <button type="submit">🔍 Szukaj</button>
            </form>
        </div>
        
        {% if keyword %}
            <div class="results-info">
                {% if count > 0 %}
                    Znaleziono {{ count }} {{ 'wynik' if count == 1 else 'wyników' if 1 < count < 5 else 'wyników' }}
                    dla frazy: <span class="highlight">{{ keyword }}</span>
                {% else %}
                    Nie znaleziono wyników dla frazy: <span class="highlight">{{ keyword }}</span>
                {% endif %}
            </div>
        {% endif %}

        {% if results %}
            <div class="results-container">
                {% for result in results %}
                    <div class="post-card">
                        <h3 class="post-title">{{ result[0] }}</h3>
                        <p class="post-content">{{ result[1] }}</p>
                    </div>
                {% endfor %}
            </div>
        {% elif keyword %}
            <div class="no-results">
                <p>Spróbuj użyć innych słów kluczowych lub zmień kryteria wyszukiwania.</p>
            </div>
        {% endif %}
    </div>
</body>
</html>
'''

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # zmień na swojego użytkownika
        password="",  # zmień na swoje hasło
        database="sqlinj"
    )

@app.route('/')
def index():
    keyword = request.args.get('keyword', '')
    results = []
    count = 0
    
    if keyword:
        try:
            conn = get_db()
            cursor = conn.cursor()
            query = f"SELECT title, post_content FROM blog WHERE post_content LIKE '%{keyword}%' AND published = 1"
            cursor.execute(query)
            results = cursor.fetchall()
            count = len(results)
            
        except mysql.connector.Error as err:
            print(f"Błąd bazy danych: {err}")
            return f"Wystąpił błąd: {err}"
            
        finally:
            if 'conn' in locals():
                conn.close()
    
    return render_template_string(TEMPLATE, results=results, count=count, keyword=keyword)

if __name__ == '__main__':
    app.run(debug=True, port=5000)