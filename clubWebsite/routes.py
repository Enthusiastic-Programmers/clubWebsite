import time
import secrets
import html
import urllib
import html
from werkzeug import unescape

import traceback
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from flask import Blueprint, render_template, send_from_directory, request, redirect, url_for, abort, Response, flash

from clubWebsite.forms import RegistrationForm
from clubWebsite.database.models import Member
from clubWebsite.config import BaseConfig

views_blueprint = Blueprint('views', __name__, template_folder='templates')

@views_blueprint.route("/")
def index():
    return render_template("index.html")
 

@views_blueprint.route("/hack")
def hack():
    return render_template("hack.html")

@views_blueprint.route("/about")
def about():
    return render_template("about.html")


@views_blueprint.route("/calendar")
def calendar():
    return render_template("calendar.html")

@views_blueprint.route("/hackathon")
def hackathon():
    return render_template("hackathon.html")

@views_blueprint.route("/hackathon_apply")
def hackathon_apply():
    return render_template("apply.html")

@views_blueprint.route("/join", methods=['GET','POST'])
def join():
    # Initialize form and check if it is valid
    form = RegistrationForm(meta={'csrf':False})
    valid = form.validate_on_submit()

    # On form submission with valid input
    if request.method == 'POST' and valid:
        confirmation_token, confirmation_time = Member.generate_confirmation_token()
        confirmation_link = request.url_root.rstrip('/') + url_for('views.confirm', confirmation_token=confirmation_token)

        html_content = 'Hi ' + html.escape(form.first_name.data) + ',<br><br>'
        html_content += 'You signed up for the Enthusiastic Programmers club. Verify that the following information is correct:<br><ul>'
        html_content += '<li>First name: ' + html.escape(form.first_name.data) + '</li>'
        html_content += '<li>Last name: ' + html.escape(form.last_name.data) + '</li>'
        html_content += '<li>Student ID: ' + html.escape(form.student_id.data) + '</li>'
        html_content += '</ul>'
        html_content += 'If the above information is correct, click this link to confirm your membership: '
        html_content += '<a href="' + html.escape(confirmation_link) + '">' + html.escape(confirmation_link) + '</a><br>'

        html_content += '''
Otherwise, simply ignore this email and submit new information on the join page. If you have already clicked the confirmation link, that is OK. Your information will be updated when you re-confirm.<br><br>

If you did not initiate this action, ignore this email.'''

        message = Mail(
            from_email='no-reply@' + request.host,
            to_emails=form.email.data,
            subject='Club membership confirmation',
            html_content=html_content
        )

        try:
            key = BaseConfig.SENDGRID_API_KEY
            if key is None:
                print("Confirmation email for %s failed. Missing SENDGRID_API_KEY." % form.first_name.data)
                abort(500)
                abort(Response('Failed to send confirmation email. Please contact the website administration.'))
            sg = SendGridAPIClient(key)
            response = sg.send(message)
        except Exception as e:
            traceback.print_exc()
            abort(500)
            abort(Response('Failed to send confirmation email. Please try again later.'))



        Member.create(form.student_id.data, form.email.data, form.first_name.data, form.last_name.data, 
                      confirmation_token=confirmation_token, confirmation_time=confirmation_time)

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
    msg = 'An email has been sent to %s to confirm your membership. You might have to check your spam folder.' % email
    
    flash(msg)
    return render_template("base.html", title="Registered")

@views_blueprint.route("/confirm")
def confirm():
    token = request.args.get('confirmation_token')
    if not token:
        abort(400)
        abort(Response('Missing confirmation token'))

    member = Member.query.filter_by(confirmation_token=token).one_or_none()
    if not member:
        flash("Invalid or expired confirmation link. Please try again.")
        return render_template("base.html", title="Membership confirmation")

    status, message = member.confirm()

    flash(message)
    return render_template("base.html", title="Membership confirmation")
