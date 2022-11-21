from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, FloatField
from wtforms.validators import DataRequired, InputRequired
from app.utils.list_images import list_images


class ImageTransformationForm(FlaskForm):
    color = FloatField('color', default=0.0, validators=[InputRequired()])
    brightness = FloatField('brightness', default=0.0, validators=[InputRequired()])
    contrast = FloatField('contrast', default=0.0, validators=[InputRequired()])
    sharpness = FloatField('sharpness', default=0.0, validators=[InputRequired()])
    image = SelectField('image', choices=list_images(), validators=[DataRequired()])
    submit = SubmitField('Submit')
