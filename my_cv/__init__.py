from flask import Flask, render_template
import os

from . import blueprints


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    @app.route('/')
    def index():
        counter = 0
        filename = os.path.join('instance', 'counter.txt')
        if os.path.isfile(filename):
            with open(filename) as file:
                counter = int(file.read())

        counter += 1
        with open(filename, 'w+') as file:
            file.write(str(counter))

        return render_template('index.html', counter=counter)

    for module_ in dir(blueprints):
        module_obj = getattr(blueprints, module_)
        if hasattr(module_obj, 'bp'):
            app.register_blueprint(getattr(module_obj, 'bp'))

    return app
