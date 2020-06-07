from flask import url_for, redirect


def page_not_found(e):
    return redirect(url_for('main.render_main')), 404


def method_not_allowed(e):
    return redirect(url_for('main.render_main')), 405
