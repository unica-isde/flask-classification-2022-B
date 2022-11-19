import redis
import os 
import re
import time

from random import randint
from utils.utils import cleanup_temp_image
from flask import render_template, request, flash, redirect
from werkzeug.utils import secure_filename
from rq import Connection, Queue
from rq.job import Job
from app import app
from app.forms.classification_upload_form import ClassificationUploadForm
from ml.classification_utils import classify_image
from config import Configuration

config = Configuration()


@app.route('/classifications_upload', methods=['GET', 'POST'])
def classifications_upload():
    """
    API that allows the user to upload an image and classify it.
    The image is temporarily saved on the server and when the job 
    is completed by the worker, it will be deleted.
    The API checks if the user has actually uploaded an image and afterwards 
    if it passes all security validations it is classified,
    otherwise the page is reloaded showing a message error.
    """

    form = ClassificationUploadForm()
    if request.method == "POST":  # POST
        model_id = form.model.data
    
        # Check if the POST request has the file parameter
        if 'uploaded_image' not in request.files:
            flash('No file has been uploaded')
            return redirect(request.url)
        
        # Check if a file has been uploaded
        if request.files['uploaded_image'].filename == '':
            flash('No file has been uploaded')
            return redirect(request.url)

        file = request.files['uploaded_image']
    
        # Security checks
        if file and allowed_file(file):
            file.filename = secure_filename(file.filename)
            image_id = save_image(file)

            redis_url = Configuration.REDIS_URL
            redis_conn = redis.from_url(redis_url)
            with Connection(redis_conn):
                q = Queue(name=Configuration.QUEUE)
                job = Job.create(
                    classify_image,
                    kwargs={
                        "model_id": model_id,
                        "img_id": image_id
                    },
                    on_failure=cleanup_temp_image,
                    on_success=cleanup_temp_image
                )
                task = q.enqueue_job(job)

                # returns the image classification output from the specified model
                # return render_template('classification_output.html', image_id=image_id, results=result_dict)
                return render_template("classification_output_queue.html", image_id=image_id, jobID=task.get_id())
        else:
            flash('File not allowed, you can upload only JPG, PNG, JPEG files')
            return redirect(request.url)

    return render_template('classification_upload.html', form=form)

def save_image(file):
    """
    Temporarily saves an uploaded image on the filesystem (/static/imagenet_subset), 
    so that it can be classified
    """
    filename = 'uploaded_' + str(time.time_ns())
    file.save(os.path.join('app/static/imagenet_subset/', filename))
    return filename

def allowed_file(file):
    """
    Validates an uploaded images, in order to be sure that 
    it is not a malicious file. Allowed files are JPEG, JPG, PNG 
    """
    # Check Content-Type
    reg = re.compile(r'image\/(png|jpg|jpeg)', re.IGNORECASE)
    if not bool(reg.search(file.content_type)):
        return False

    # Check Extension
    allowed_extensions = ['.jpg', '.png', '.jpeg']
    filename = file.filename
    while('.' in filename):
        filename = os.path.splitext(filename)
        if filename[1].lower() not in allowed_extensions:
            return False

        filename = filename[0]
    
    return True