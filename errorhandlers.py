from werkzeug.utils import redirect

from app import app


@app.errorhandler(404)
def page_not_found(e):
    return '404 error', 404


@app.errorhandler(405)
def page_not_found(e):
    return redirect('/'), 405
