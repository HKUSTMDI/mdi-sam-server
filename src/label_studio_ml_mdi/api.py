import logging

from flask import Flask, request, jsonify

from .model import LabelStudioMLBase
from .exceptions import exception_handler


logger = logging.getLogger("api")
logger.setLevel(logging.DEBUG)

# log_formatter = '%(asctime)s [%(levelname)s] [%(filename)s] [line:%(lineno)d] %(message)s'
# stream_handler = logging.StreamHandler()
# stream_handler.setFormatter(logging.Formatter(log_formatter))
# stream_handler.setLevel(logging.DEBUG)

# logger.addHandler(stream_handler)


_server = Flask(__name__)
MODEL_CLASS = LabelStudioMLBase


def init_app(model_class):
    global MODEL_CLASS
    
    if not issubclass(model_class, LabelStudioMLBase):
        raise ValueError('Inference class should be the subclass of ' + LabelStudioMLBase.__class__.__name__)

    MODEL_CLASS = model_class
    logger.debug("init ok")
    return _server


@_server.route('/predict', methods=['POST'])
@exception_handler
def _predict():
    """
    Predict tasks

    @return:
    Predictions in LS format
    """
    data = request.json
    tasks = data.get('tasks')
    params = data.get('params') or {}
    project = data.get('task_id')
    if project:
        project_id = data.get('task_id')
    else:
        project_id = None
    label_config = data.get('label_config')
    context = params.pop('context', {})

    model = MODEL_CLASS(project_id)
    model.use_label_config(label_config)

    predictions = model.predict(tasks, context=context, **params)
    return jsonify({'results': predictions})


@_server.route('/setup', methods=['POST'])
@exception_handler
def _setup():
    data = request.json
    project_id = data.get('task_id')
    label_config = data.get('schema')
    model = MODEL_CLASS(project_id)
    model.use_label_config(label_config)
    model_version = model.get('model_version')
    return jsonify({'model_version': model_version})


TRAIN_EVENTS = (
    'ANNOTATION_CREATED',
    'ANNOTATION_UPDATED',
    'ANNOTATION_DELETED',
    'PROJECT_UPDATED'
)

@_server.route('/health', methods=['GET'])
@_server.route('/', methods=['GET'])
@exception_handler
def health():
    return jsonify({
        'code': 200,
        'msg': 'ok',
        'model_class': MODEL_CLASS.__name__
    })

@_server.errorhandler(FileNotFoundError)
def file_not_found_error_handler(error):
    logger.warning('Got error: ' + str(error))
    return str(error), 404


@_server.errorhandler(AssertionError)
def assertion_error(error):
    logger.error(str(error), exc_info=True)
    return str(error), 500


@_server.errorhandler(IndexError)
def index_error(error):
    logger.error(str(error), exc_info=True)
    return str(error), 500


@_server.before_request
def log_request_info():
    logger.debug('Request headers: %s', request.headers)
    logger.debug('Request body: %s', request.get_data())


@_server.after_request
def log_response_info(response):
    logger.debug('Response status: %s', response.status)
    logger.debug('Response headers: %s', response.headers)
    logger.debug('Response body: %s', response.get_data())
    return response
