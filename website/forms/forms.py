import logging
from flask_wtf import FlaskForm
from wtforms import Form, BooleanField, StringField, PasswordField, validators, SelectField, DateField, DateTimeField
from wtforms import validators
from wtforms.validators import InputRequired, Email
from wtforms import PasswordField, ValidationError
from database.database import db


class RegistrationForm(FlaskForm):
	username = StringField('Username', [
		validators.Length(min=6, max=35), InputRequired("Please enter a username.")
	])
	first_name = StringField('First name', [
		validators.Length(min=2, max=35), InputRequired("Please enter your first name.")
	])
	last_name = StringField('Last name', [
		validators.Length(min=2, max=35), InputRequired("Please enter your last name.")
	])
	
	password = PasswordField('Password', [
		validators.InputRequired("Please enter your password."),
		validators.Length(min=9),
		validators.EqualTo('confirm', message='Passwords must match')
	])
	confirm = PasswordField('Repeat Password')
	
	def validate(self, extra_validators=None):
		if super().validate(extra_validators):
			from database.models import User
			user = db.session.query(User).filter_by(username=self.username.data).first()

			if user is not None:
				logging.warning("User with this username already exists.")
				return False
			
			return True

		return False


class LoginForm(FlaskForm):
	username = StringField('Username', [
		validators.Length(min=6, max=35), InputRequired("Please enter a username.")
	])
	password = PasswordField('Password', [
		validators.InputRequired("Please enter your password."),
		validators.Length(min=9)
	])
	
	def validate(self, extra_validators=None):
		if super().validate(extra_validators):
			return True
		return False


class ChangePasswordForm(FlaskForm):
	old_password = PasswordField('Current Password', [
		validators.InputRequired("Please enter your current password."),
		validators.Length(min=9)
	])
	new_password = PasswordField('New Password', [
		validators.InputRequired("Please enter your new password."),
		validators.Length(min=9),
		validators.EqualTo('confirm_new', message='Passwords must match')
	])
	confirm_new = PasswordField('Repeat New Password')
	
	def validate(self, extra_validators=None):
		if super().validate(extra_validators):
			return True
		return False
