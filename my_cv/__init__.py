from flask import Flask, render_template

from . import blueprints


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template('index.html')

    for module_ in dir(blueprints):
        module_obj = getattr(blueprints, module_)
        if hasattr(module_obj, 'bp'):
            app.register_blueprint(getattr(module_obj, 'bp'))

    return app
