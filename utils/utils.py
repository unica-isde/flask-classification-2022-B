import os

from config import Configuration

conf = Configuration()

def cleanup_temp_image(job, connection, result, *args, **kwargs):
    """
    It's called by a worker when it completes successfully or not
    a job. It removes the image, which was temporary saved on the
    server during upload phase, associated to the job 
    """
    os.remove(
        os.path.join(
            conf.image_folder_path, 
            job.kwargs['img_id']
        )
    )
