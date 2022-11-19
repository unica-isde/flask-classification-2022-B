import os

from config import Configuration

conf = Configuration()

def cleanup_temp_image(job, connection, result, *args, **kwargs):
    os.remove(os.path.join(conf.image_folder_path, job.kwargs['img_id']))
