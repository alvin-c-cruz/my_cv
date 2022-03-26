from flask import Blueprint, render_template, request, current_app
import subprocess
import os

bp = Blueprint('hello_world', __name__, template_folder='pages', url_prefix='/hello')


@bp.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        code = request.form['code']

        file_path = os.path.join(current_app.instance_path, 'temp', 'hello.py')
        with open(file_path, 'w+') as file:
            file.write(code)

        command = f'python {file_path}'
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        output = output.decode().replace('b"', '')
        print(output, type(output))
    else:
        code = ""
        output = ""
        error = ""
    return render_template('hello_world/home.html', code=code, output=output, error=error)
