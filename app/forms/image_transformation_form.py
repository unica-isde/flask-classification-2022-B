from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, FloatField
from wtforms.validators import DataRequired
from app.utils.list_images import list_images


class ImageTransformationForm(FlaskForm):
    color = FloatField('color', default=0, validators=[DataRequired()])
    brightness = FloatField('brightness', default=0, validators=[DataRequired()])
    contrast = FloatField('contrast', default=0, validators=[DataRequired()])
    sharpness = FloatField('sharpness', default=0, validators=[DataRequired()])
    image = SelectField('image', choices=list_images(), validators=[DataRequired()])
    submit = SubmitField('Submit')
