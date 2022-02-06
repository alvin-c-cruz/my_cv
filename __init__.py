from flask import Flask
from flask_migrate import Migrate
from flask_security import Security, SQLAlchemyUserDatastore
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_security.forms import RegisterForm, ConfirmRegisterForm
from wtforms import StringField, DateField

import os


db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(app.instance_path, "data.db")
    app.config.from_pyfile("config.py")
    app.config.from_pyfile("mail_config.cfg")

    from . import blueprints
    for module_ in dir(blueprints):
        module_obj = getattr(blueprints, module_)
        if hasattr(module_obj, 'bp'):
            app.register_blueprint(getattr(module_obj, 'bp'))

    db.init_app(app)
    if not os.path.isfile(os.path.join(app.instance_path, "data.db")):
        with app.app_context():
            db.create_all()

    mail = Mail(app)

    class ExtendedRegisterForm(RegisterForm):
        name = StringField('Name')
        birthday = DateField('Birthday')

    class ExtendedConfirmRegisterForm(ConfirmRegisterForm):
        name = StringField('Name')
        birthday = DateField('Birthday')

    user_datastore = SQLAlchemyUserDatastore(db, blueprints.auth.User, blueprints.auth.Role)
    security = Security(app, user_datastore,
                        register_form=ExtendedRegisterForm,
                        confirm_register_form=ExtendedConfirmRegisterForm)
    migrate.init_app(app, db)

    return app
