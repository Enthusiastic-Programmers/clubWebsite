import time
import secrets
import html
import urllib
from werkzeug import unescape

from flask import Blueprint, render_template, send_from_directory, request, redirect, url_for, abort, Response

from clubWebsite.forms import RegisterForm
from clubWebsite.database.models import Member

views_blueprint = Blueprint('views', __name__, template_folder='templates')

@views_blueprint.route("/")
def index():
    return render_template("index.html")

@views_blueprint.route("/faq")
def faq():
    return render_template("faq.html")

@views_blueprint.route("/about")
def about():
    return render_template("about.html")

@views_blueprint.route("/contact")
def contact():
    return render_template("contact.html")

@views_blueprint.route("/join", methods=['GET','POST'])
def join():
    # Initialize form and check if it is valid
    form = RegisterForm() 
    valid = form.validate_on_submit()

    # On form submission with valid input
    if request.method == 'POST' and valid:
        #print(form.email.data, form.student_id.data, form.first_name.data, form.last_name.data, time_added, confirmation_token, False)
        Member.get_or_create(form.student_id.data, form.email.data, form.first_name.data, form.last_name.data)

        # Redirect to email_sent page
        return redirect(url_for('views.email_sent', email=form.email.data))
    
    # Render form template when method is GET, or form is not valid
    return render_template("join.html", form=form)

@views_blueprint.route("/email_sent")
def email_sent():
    email = request.args.get('email')
    if not email:
        abort(400)
        abort(Response('Missing email'))
    msg = 'An email has been sent to %s to confirm your membership'
    # TODO: Send confirmation email here
    return render_template("template.html", title="Success", main=msg%(email))

@views_blueprint.route("/confirm")
def confirm():
    student_id = request.args.get('id')
    token = request.args.get('confirmation_token')
    if not token or not student_id:
        abort(400)
        abort(Response('Missing student id or confirmation token'))

    member = Member.query.get(int(student_id))
    if not member:
        abort(400)
        abort(Response("Invalid student id"))

    status, message = member.confirm(token)
    return render_template("template.html", title="Membership confirmation", main=message)