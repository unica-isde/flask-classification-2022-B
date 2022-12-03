from flask import render_template
from app.forms.histogram_form import HistogramForm
from app import app
from config import Configuration

conf = Configuration()


@app.route('/histogram', methods=['GET', 'POST'])
def histogram():
    """API for selecting an image and returning
    the view page of the image histogram.
    """
    form = HistogramForm()
    if form.validate_on_submit():  # POST
        image_id = form.image.data
        # returns the view page for the image selected
        return render_template('histogram_output.html', image_id=image_id)
    # otherwise, it is a get request and should return the
    # image selector
    return render_template('image_histogram.html', form=form)