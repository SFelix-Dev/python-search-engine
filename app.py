import sqlite3
import re
from flask import Flask, render_template, request

app = Flask(__name__)

DB_NAME = "app.db"


# -----------------------------
# DATABASE SETUP
# -----------------------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM documents")
    count = cursor.fetchone()[0]

    # seed data only if empty
    if count == 0:
        sample_docs = [
            "python is easy to learn",
            "data structures are important",
            "flask is a web framework",
            "coding builds problem solving skills",
            "search engines use indexing"
        ]

        for doc in sample_docs:
            cursor.execute("INSERT INTO documents (content) VALUES (?)", (doc,))

    conn.commit()
    conn.close()


# -----------------------------
# LOAD DOCUMENTS FROM DB
# -----------------------------
def load_documents():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT content FROM documents")
    rows = cursor.fetchall()

    conn.close()

    return [row[0] for row in rows]


# -----------------------------
# BUILD INVERTED INDEX
# -----------------------------
inverted_index = {}


def build_index(documents):
    inverted_index.clear()

    for doc in documents:
        words = re.findall(r'\w+', doc.lower())

        for word in words:
            if word not in inverted_index:
                inverted_index[word] = []
            inverted_index[word].append(doc)


# -----------------------------
# SEARCH FUNCTION
# -----------------------------
def search(query):
    query_words = re.findall(r'\w+', query.lower())

    results = {}

    for word in query_words:
        if word in inverted_index:
            for doc in inverted_index[word]:
                results[doc] = results.get(doc, 0) + 1

    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)

    return [doc for doc, score in sorted_results]


# -----------------------------
# INIT APP
# -----------------------------
init_db()
documents = load_documents()
build_index(documents)


# -----------------------------
# ROUTES
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def home():
    results = []

    if request.method == "POST":
        query = request.form.get("query", "")
        results = search(query)

    return render_template("index.html", results=results)


# -----------------------------
# RUN APP
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

    