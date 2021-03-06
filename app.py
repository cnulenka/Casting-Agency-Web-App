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

app = Flask(__name__)

if __name__ == "__main__":
    app.run()