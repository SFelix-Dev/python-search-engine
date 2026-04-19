
import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM documents")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.execute("INSERT INTO documents (content) VALUES ('python is easy to learn')")
        cursor.execute("INSERT INTO documents (content) VALUES ('data structures are important')")
        cursor.execute("INSERT INTO documents (content) VALUES ('flask is a web framework')")
        cursor.execute("INSERT INTO documents (content) VALUES ('coding builds problem solving skills')")
        cursor.execute("INSERT INTO documents (content) VALUES ('search engines use indexing')")

    conn.commit()
    conn.close()

init_db()

documents = [
    "python should be everyones first programming language, its easyy to learn",
    "data structures are important",
    "flask is a web framework",
    "coding builds problem solving skills",
    "search engines use indexing"
]

inverted_index = {}

def build_index():
    for i, doc in enumerate(documents):
        words = doc.lower().split()

        for word in words:
            if word not in inverted_index:
                inverted_index[word] = []

            inverted_index[word].append(doc)

build_index()

def search(query):
    query_words = query.lower().split()

    results = {}

    for word in query_words:
        if word in inverted_index:
            for doc in inverted_index[word]:
                results[doc] = results.get(doc, 0) + 1

    # sort by relevance score
    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)

    return [r[0] for r in sorted_results]

@app.route('/', methods=['GET', 'POST'])
def home():
    results = []

    if request.method == 'POST':
        query = request.form['query']
        results = search(query)

    return render_template("index.html", results=results)


if if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)