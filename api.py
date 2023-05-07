import json
import wsgiserver
from predict_from_abstract import split_into_sentences, predict_sentences


def application(environ, start_response):
    if environ['REQUEST_METHOD'] != 'POST':
        start_response('405 Method Not Allowed', [('Content-type', 'text/plain'), ('Access-Control-Allow-Origin', '*')])
        return [b'Only POST requests are allowed.']

    request_body = environ['wsgi.input'].read(int(environ['CONTENT_LENGTH'])).decode('utf-8')
    print(request_body)
    sentences = split_into_sentences(request_body)
    percentages = predict_sentences(sentences)
    print(percentages)

    # Set the response headers
    status = '200 OK'
    response_body = json.dumps([sentences, percentages])
    response_headers = [('Content-type', 'text/plain'),
                        ('Content-Length', str(len(response_body))),
                        ('Access-Control-Allow-Origin', '*'),
                        ('Access-Control-Allow-Methods', 'POST'),
                        ('Access-Control-Allow-Headers', 'Content-Type')]
    start_response(status, response_headers)

    return [response_body.encode('utf-8')]


server = wsgiserver.WSGIServer(application, port=8001)
server.start()
