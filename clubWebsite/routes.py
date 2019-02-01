from flask import render_template, send_from_directory, request

from clubWebsite import app

@app.route("/")
@app.route("/index")
@app.route("/index.html")
def index():
    return render_template("index.html")

@app.route("/faq")
@app.route("/faq.html")
def faq():
    return render_template("faq.html")

@app.route("/about")
@app.route("/about.html")
def about():
    return render_template("about.html")

@app.route("/about")
@app.route("/contact.html")
def contact():
    return render_template("contact.html")

@app.route("/join")
@app.route("/join.html")
def join():
    return render_template("join.html")

