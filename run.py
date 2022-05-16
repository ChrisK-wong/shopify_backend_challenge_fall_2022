from api import create_app
app = create_app()

from frontend.web import web
app.register_blueprint(web)

app.run(debug=True)
