from flask import redirect, url_for


def create_webapp(app):
    from .web import web
    app.register_blueprint(web)

    @app.route('/', methods=['GET'])
    def index():
        return redirect(url_for('web.index'))
