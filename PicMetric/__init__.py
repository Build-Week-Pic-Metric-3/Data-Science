from .app import create_app

APP = create_app()
APP.run(debug=False,host="0.0.0.0")
