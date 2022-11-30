from flask import render_template
from app.forms.histogram_form import HistogramForm
from app import app
from config import Configuration

conf = Configuration()


@app.route('/histogram', methods=['GET', 'POST'])
def histogram():
    form = HistogramForm()
    if form.validate_on_submit():  # POST
        image_id = form.image.data
        return render_template('histogram_output.html', image_id=image_id)
    return render_template('image_histogram.html', form=form)