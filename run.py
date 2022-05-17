from api import create_app
app = create_app()

from frontend import create_webapp
create_webapp(app)

app.run()
