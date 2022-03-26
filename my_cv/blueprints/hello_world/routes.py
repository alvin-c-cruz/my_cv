from flask import Blueprint, render_template, request, current_app
import subprocess
import sys

bp = Blueprint('hello_world', __name__, template_folder='pages', url_prefix='/hello')


@bp.route('/', methods=['POST', 'GET'])
def home():
    code = 'print("Hello World!")'
    output = ""

    if request.method == 'POST':
        code = request.form['code']

        if 'import' in code:
            pass
        else:
            process_output = subprocess.run(
                [sys.executable, "-c", code], capture_output=True, text=True
                )

            if process_output.stderr:
                output = process_output.stderr.replace('File "<string>", ', '')
            else:
                output = process_output.stdout

    return render_template('hello_world/home.html', code=code, output=output)
