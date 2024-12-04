from flask import Flask, render_template, request, redirect, url_for, flash
import random
import string
import sqlite3

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with a secure key

# Database setup
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS urls (id INTEGER PRIMARY KEY, long_url TEXT, short_url TEXT)''')
    conn.commit()
    conn.close()

# Function to generate a random short URL
def generate_short_url():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

# Home page route
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        long_url = request.form.get("long_url")
        if not long_url:
            flash("Please provide a URL!", "error")
            return redirect(url_for("home"))

        # Check if URL already exists
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT short_url FROM urls WHERE long_url = ?", (long_url,))
        result = c.fetchone()

        if result:
            short_url = result[0]
        else:
            short_url = generate_short_url()
            c.execute("INSERT INTO urls (long_url, short_url) VALUES (?, ?)", (long_url, short_url))
            conn.commit()
        
        conn.close()
        return render_template("short_url.html", short_url=short_url)

    return render_template("home.html")

# Redirect short URL to long URL
@app.route("/<short_url>")
def redirect_to_long_url(short_url):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT long_url FROM urls WHERE short_url = ?", (short_url,))
    result = c.fetchone()
    conn.close()

    if result:
        return redirect(result[0])
    else:
        flash("Short URL not found!", "error")
        return redirect(url_for("home"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
