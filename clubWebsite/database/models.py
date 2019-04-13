"""Database ORM models"""
import datetime
import secrets
import os

from clubWebsite.database import db

class Member(db.Model):
    """Member of the club who has signed up"""
    __tablename__ = 'members'
    member_id = db.Column(db.Integer, nullable=False, index=True, primary_key=True)  #: Internal SQL id
    student_id = db.Column(db.Integer, nullable=False, index=True)                   #: Student's ID number (900xxxxxxx)
    email = db.Column(db.String(128), nullable=False, index=True)                    #: Student's e-mail address (@my.vcccd.edu)
    first_name = db.Column(db.String(64), nullable=False)                            #: Student's first name
    last_name = db.Column(db.String(64), nullable=False)                             #: Student's last name
    time_added = db.Column(db.DateTime(), default=datetime.datetime.utcnow)          #: Datetime (in UTC) when the registration occurred
    confirmation_token = db.Column(db.String(64), index=True, unique=True)           #: Generated confirmation token
    confirmation_time = db.Column(db.DateTime())                                     #: When the confirmation token was sent (used to calculate token expiry)
    is_confirmed = db.Column(db.Boolean(), default=False)                            #: Boolean flag, is True once the student has confirmed their membership

    def __init__(self, student_id, email, first_name, last_name, confirmation_token=None, confirmation_time=None, **kwargs):
        self.email = email
        self.student_id = student_id
        self.first_name = first_name
        self.last_name = last_name
        if confirmation_token is not None:
            self.confirmation_token = confirmation_token
        if confirmation_time is not None:
            self.confirmation_time = confirmation_time
        super(Member, self).__init__(**kwargs)

    def __repr__(self):
        status = "Confirmed" if self.is_confirmed else "Not Confirmed"
        return "<Member {}, {}, {}>".format(self.student_id, self.first_name, status)

    @staticmethod
    def create(student_id, email, first_name, last_name, **kwargs):
        """Create a new Member with the given parameters"""
        new_member = Member(student_id, email, first_name, last_name, **kwargs)
        db.session.add(new_member)
        db.session.commit()

        return new_member

    @staticmethod
    def prune_expired(expire_delta=48):
        """Delete members who haven't confirmed their e-mails within expire_delta hours"""
        delete_ids = []
        for member in Member.query.filter_by(is_confirmed=False).all():
            if member.has_token_expired(expire_delta):
                delete_ids.append(member.student_id)
        Member.query.delete(delete_ids)
        db.session.commit()

    @staticmethod
    def generate_confirmation_token():
        """Generates a confirmation token"""
        confirmation_token = secrets.token_urlsafe(nbytes=32)
        confirmation_time = datetime.datetime.utcnow()
        return confirmation_token, confirmation_time

    def confirm(self, expire_delta=48):
        """
        Confirms the membership with the given token. Defaults to 48h expiry period
        Returns a boolean with success/failure, and a string with verbose output
        """
        if self.is_confirmed:
            # Already confirmed
            return True, "Your membership has already been confirmed"

        elif self.has_token_expired(expire_delta):
            # Token expired
            return False, "Confirmation link expired, please try again"

        else:
            self.is_confirmed = True

            # Remove any other entries with this email address - they are either fake or outdated
            for member in Member.query.filter(Member.email == self.email, Member.member_id != self.member_id).all():
                db.session.delete(member)

            db.session.commit()
            return True, "Your membership has been confirmed"


    def get_token_expire_time(self, expire_delta):
        """Get the time at which the confirmation token will expire """
        return self.confirmation_time + datetime.timedelta(hours=expire_delta)

    def has_token_expired(self, expire_delta):
        """Test if the current token has expired yet"""
        expire_time = self.get_token_expire_time(expire_delta)
        time_left = (expire_time - datetime.datetime.utcnow()).total_seconds()
        return time_left <= 0
