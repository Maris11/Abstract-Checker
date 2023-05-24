import json
import wsgiserver
from predict_from_abstract import split_into_sentences, predict_sentences, get_language


def application(environ, start_response):
    if environ['REQUEST_METHOD'] != 'POST':
        start_response('405 Method Not Allowed', [('Content-type', 'text/plain')])
        return [b'Only POST requests are allowed.']

    request_body = environ['wsgi.input'].read(int(environ['CONTENT_LENGTH'])).decode('utf-8')
    request_body = json.loads(request_body)
    language = request_body[0]
    abstract = request_body[1]

    if language == "auto":
        language = get_language(abstract)

    print(language, abstract)
    sentences = split_into_sentences(abstract, language)
    percentages = predict_sentences(sentences, language)
    print(percentages)

    # Set the response headers
    status = '200 OK'
    response_body = json.dumps([sentences, percentages, language])
    response_headers = [('Content-type', 'text/plain'),
                        ('Content-Length', str(len(response_body))),
                        ('Access-Control-Allow-Origin', '*'),
                        ('Access-Control-Allow-Methods', 'POST'),
                        ('Access-Control-Allow-Headers', 'Content-Type')]
    start_response(status, response_headers)

    return [response_body.encode('utf-8')]


server = wsgiserver.WSGIServer(application, port=8001)
server.start()
