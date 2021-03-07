import flask
import json
from cerberus import Validator
import traceback
from algorithm import main_function

input_schema = {
    'githubOwnerName': {'type': 'string'},
    'githubProjectName': {'type': 'string'},
}


def prepare_error_response(ERROR:str, event:dict)-> dict:
    '''
    returns error response in case of error
    '''
    error_response = {
        'githubOwnerName': event['githubOwnerName'],
        'githubProjectName': event['githubProjectName'],
        'errorMessage': str(ERROR)
    }
    return error_response

def prediction_handler(event:dict, context=None)->dict:

    valid_output = Validator(input_schema)

    # check if the task is dict format
    if not isinstance(event, dict):
        response_message = prepare_error_response('ValueError',event)
    else:
        status = valid_output.validate(event, input_schema)
        if status:
            response_message = main_function(event.get('githubOwnerName'),event.get('githubProjectName'))

        else:
            error = json.dumps({'error': valid_output.errors})
            response_message = prepare_error_response(error, event)
    return response_message


# The flask app for serving predictions
app = flask.Flask(__name__)

@app.route('/getStarCountData', methods=['GET'])
def get_extraction():
    if flask.request.content_type == 'application/json':
        event = flask.request.get_json()
    else:
        return flask.Response(
            response='This predictor only supports JSON data\n',
            status=415,
            mimetype='application/json')

    try:
        response = prediction_handler(event)
        result = json.dumps(response)
        print(result)
        return flask.Response(response=result,
                              status=200,
                              mimetype='application/json')
    
    except BaseException as ERROR:
        error_response = prepare_error_response(str(ERROR), event)
        print(ERROR)
        print(traceback.format_exc())
        return flask.Response(response=error_response,
                              status=500,
                              mimetype='application/json')


if __name__ == "__main__":
    # main place where the flask app runs
    app.run(host='0.0.0.0', port=9300)
