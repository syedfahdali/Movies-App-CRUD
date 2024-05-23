import logging
from website.appCreator import app


if __name__ == '__main__':
    development_warning = "WARNING: This is a development server. Do not use it in a production deployment. " \
                          "Use a production WSGI server instead."

    local_host_ip = "127.0.0.1"

    logging.info(logging.WARNING, f" * Running on http://{local_host_ip}:{80},", "red")
    app.run(host=local_host_ip, port=80,debug=True)
