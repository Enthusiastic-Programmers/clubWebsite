import time
import secrets
import html
import urllib
from werkzeug import unescape

from flask import render_template, send_from_directory, request, redirect, url_for, abort, Response

from clubWebsite import app
from clubWebsite.forms import RegisterForm
from clubWebsite.database import _confirm_member, _add_member

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/faq")
def faq():
    return render_template("faq.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/join", methods=['GET','POST'])
def join():
    # Initialize form and check if it is valid
    form = RegisterForm() 
    valid = form.validate_on_submit()

    # On form submission with valid input
    if request.method == 'POST' and valid:
        time_added = time.time()

        # Confirmation code to be used in email confirmation link
        confirmation_token = str(time_added) + '_' + secrets.token_urlsafe(nbytes=32)

        # Now add the person to the members table
        print(form.email.data, form.student_id.data, form.first_name.data, form.last_name.data, time_added, confirmation_token, False)
        _add_member(form.email.data, form.student_id.data, form.first_name.data, form.last_name.data, time_added, confirmation_token, False)

        # Redirect to email_sent page
        return redirect(url_for('email_sent', email=form.email.data))
    
    # Render form template when method is GET, or form is not valid
    return render_template("join.html", form=form)

@app.route("/email_sent")
def email_sent():
    email = request.args.get('email')
    if not email:
        abort(400)
        abort(Response('Missing email'))
    msg = 'An email has been sent to %s to confirm your membership'
    return render_template("template.html", title="Success", main=msg%(email))

@app.route("/confirm")
def confirm():
    token = request.args.get('confirmation_token')
    if not token:
        abort(400)
        abort(Response('Missing confirmation token'))
    message = _confirm_member(token)
    return render_template("template.html", title="Membership confirmation", main=message)