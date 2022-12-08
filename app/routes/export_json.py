import json
from app import app
from flask import Response
from .classifications_id import classifications_id


@app.route('/export_json/<string:job_id>', methods=['GET'])
def export_json(job_id):
    """
    API for downloading the result of the classification
    in JSON format
    """
    response = classifications_id(job_id)

    raw_json = {info[0]: info[1] for info in response['data']}

    return Response(
            json.dumps(
                raw_json, 
                indent=4
            ),
            mimetype='application/json',
            headers={
                'Content-disposition':
                "attachment; filename=results_" + job_id + ".json"
            }
        )