from flask import Flask, render_template, request, redirect, flash, session
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

def get_user_by_email(email):
    conn = sqlite3.connect("jallow_world.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cur.fetchone()
    conn.close()
    return user

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
        return redirect("/login")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = get_user_by_email(email)
        if user and user[4] == password:  # Vérifier que le mot de passe est correct (user[4] est le mot de passe)
            session["user_id"] = user[0]  # Stocker l'ID de l'utilisateur dans la session
            flash("Connexion réussie !")
            return redirect("/")
        else:
            flash("Email ou mot de passe incorrect.")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user_id", None)  # Retirer l'utilisateur de la session
    flash("Déconnexion réussie !")
    return redirect("/login")

@app.route("/")
def home():
    return "<h1>Bienvenue sur Jallow World !</h1>"

if __name__ == "__main__":
    create_db()
    app.run(debug=True)
