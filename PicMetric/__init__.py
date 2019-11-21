from .app import create_app

#may require tinkering depending on how gunicron is set up

APP = create_app()
APP.run(host="0.0.0.0")