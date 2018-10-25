from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, TextAreaField, SelectField
from wtforms.validators import  DataRequired
from .lookup import *


class AddTrackerForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    priority = SelectField('Priority', choices = Lookup(PRIORITIES))
    submit = SubmitField('Submit')


class EditTrackerForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    status = SelectField('Status', choices =Lookup(STATUSES))
    priority = SelectField('Priority', choices =Lookup(PRIORITIES))
    submit = SubmitField('Submit')
