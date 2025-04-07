from flask import Flask, render_template, request, redirect, flash
import sqlite3
from models import create_db

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.secret_key = app.config['SECRET_KEY']

def insert_user(nom, pseudo, email, password):
    conn = sqlite3.connect("jallow_world.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO users (nom, pseudo, email, password) VALUES (?, ?, ?, ?)",
                (nom, pseudo, email, password))
    conn.commit()
    conn.close()

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nom = request.form["nom"]
        pseudo = request.form["pseudo"]
        email = request.form["email"]
        confirm_email = request.form["confirm_email"]
        password = request.form["password"]

        if email != confirm_email:
            flash("Les emails ne correspondent pas.")
            return render_template("register.html")
        
        insert_user(nom, pseudo, email, password)
        flash("Inscription réussie !")
        return redirect("/")

    return render_template("register.html")

@app.route("/")
def home():
    return "<h1>Bienvenue sur Jallow World !</h1>"

if __name__ == "__main__":
    create_db()
    app.run(debug=True)
