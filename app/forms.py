from flask_wtf import Form
from wtforms import StringField, BooleanField, PasswordField, FileField, HiddenField, DateField, SelectField, TextAreaField, IntegerField, RadioField, FieldList, FormField, SubmitField
from wtforms.validators import Required, Optional, NumberRange, Email, EqualTo

# Login Form class with form validation
class LoginForm(Form):
  email = StringField('email', validators = [Required()])
  password = PasswordField('password', validators = [Required()])
  remember_me = BooleanField('remember_me', default = False)


# Sign Up Form class with form validation
class SignUpForm(Form):
  first_name = StringField('first_name', validators = [Required()])
  last_name = StringField('last_name', validators = [Required()])
  email = StringField('email', validators = [Required(), Email()]) 
  password = PasswordField('password', validators = [Required(), EqualTo('confirm', message = 'Passwords must match')])
  confirm = PasswordField('Repeat Password')
