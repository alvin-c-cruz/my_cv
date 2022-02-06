from flask import Blueprint, render_template
from flask_security import login_required, roles_accepted

bp = Blueprint('home_page', __name__, template_folder="pages")


@bp.route("/")
def landing_page():
    return render_template('home_page/landing_page.html')


@bp.route("/home")
@login_required
@roles_accepted('admin', 'viewer', 'editor')
def home():
    return render_template('home_page/home.html')
