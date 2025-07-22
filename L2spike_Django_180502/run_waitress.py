import logging
from waitress import serve
from L2spike_Django_180502.wsgi import application

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    serve(application, host='0.0.0.0', port=8001)