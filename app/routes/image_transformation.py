from flask import render_template
from app import app
from app.forms.image_transformation_form import ImageTransformationForm
from ml.classification_utils import fetch_image
from PIL import ImageEnhance


@app.route('/image-transformation', methods=['GET', 'POST'])
def image_transformation():
    form = ImageTransformationForm()
    if form.validate_on_submit():
        color = form.color.data
        brightness = form.brightness.data
        contrast = form.contrast.data
        sharpness = form.sharpness.data

        image_id = form.image.data

        image = fetch_image(image_id)
        enhancer_color = ImageEnhance.Color(image)
        image_with_color = enhancer_color.enhance(color)
        enhancer_brightness = ImageEnhance.Brightness(image_with_color)
        image_with_brightness = enhancer_brightness.enhance(brightness)
        enhancer_contrast = ImageEnhance.Contrast(image_with_brightness)
        image_with_contrast = enhancer_contrast.enhance(contrast)
        enhancer_sharpness = ImageEnhance.Sharpness(image_with_contrast)
        image_with_sharpness = enhancer_sharpness.enhance(sharpness)

        transformed_image = image_with_sharpness
        transformed_image.save("app/static/imagenet_subset/transformation_"+image_id)

        return render_template("image_transformation_output.html", image_id=image_id, color=color,brightness=brightness, contrast=contrast, sharpness=sharpness)

    return render_template('image_transformation.html', form=form)
