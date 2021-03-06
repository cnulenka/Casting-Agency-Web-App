from flask import (
    Flask,
    render_template,
    request,
    Response,
    flash,
    redirect,
    url_for,
    abort,
)
from models import *

app = Flask(__name__)
setup_db(app)

if __name__ == "__main__":
    app.run()
