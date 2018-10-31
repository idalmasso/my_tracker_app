from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, MultipleFileField, TextAreaField, SelectField,SelectMultipleField
from wtforms.validators import  DataRequired
from .lookup import *


class AddTrackerForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    priority = SelectField('Priority', choices = Lookup(PRIORITIES))
    project = SelectField('Project', validators=[DataRequired()])
    categories = SelectMultipleField('Categories',choices=Lookup(CATEGORIES))
    images = MultipleFileField('Images')
    submit = SubmitField('Submit')


class EditTrackerForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    status = SelectField('Status', choices =Lookup(STATUSES))
    priority = SelectField('Priority', choices =Lookup(PRIORITIES))
    project = SelectField('Project', validators=[DataRequired()])
    categories = SelectMultipleField('Categories',choices=Lookup(CATEGORIES))
    images = MultipleFileField('Images')
    submit = SubmitField('Submit')
