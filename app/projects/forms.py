from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, TextAreaField, SelectField
from wtforms.validators import  DataRequired



class AddEditProjectForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    prefix = StringField('Prefix for trackers', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')
