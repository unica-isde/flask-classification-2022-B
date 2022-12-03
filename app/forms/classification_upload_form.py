from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.validators import DataRequired

from config import Configuration

conf = Configuration()


class ClassificationUploadForm(FlaskForm):
    model = SelectField('model', choices=conf.models, validators=[DataRequired()])
    submit = SubmitField('Submit')
