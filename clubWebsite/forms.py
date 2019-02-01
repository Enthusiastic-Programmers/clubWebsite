from flask_wtf import FlaskForm
from wtforms import validators, ValidationError
from wtforms.fields import TextField, SubmitField
from wtforms.fields.html5 import EmailField

class RegisterForm(FlaskForm):
   first_name = TextField("First Name", [validators.DataRequired()])
   
   last_name = TextField("Last Name", [validators.DataRequired()])
   
   student_id = TextField("900 number", [validators.DataRequired(),
                                         validators.Regexp(r'900\d{6}', message="Not a valid student ID")])

   email = EmailField('myVCCCD email', [validators.DataRequired(), 
                                        validators.Email()])
   submit = SubmitField("Submit")

   def validate_email(form, field):
      if not str(field.data).endswith('@my.vcccd.edu'):
         raise ValidationError('E-mail address must be @my.vcccd.edu')