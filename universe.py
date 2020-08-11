import os
from sys import argv
from flask import (
	Flask, send_from_directory, render_template, safe_join, request
)
app = Flask(__name__)

APP_ROOT = f'{os.path.dirname(__file__)}'
STATIC_ROOT = APP_ROOT + '/static'
FILES_ROOT = APP_ROOT + '/files'


def remote_addr():
	if 'X-Forwarded-For' in request.headers:
		remote_addr = request.headers.getlist("X-Forwarded-For")[0].rpartition(' ')[-1]
	else:
		remote_addr = request.remote_addr or 'untrackable'
	return remote_addr


@app.route('/css/<path:stylesheet>')
def serve_css(stylesheet):
	return send_from_directory(f'{STATIC_ROOT}/css', stylesheet)


@app.route('/ttf/<path:fontfile>')
def serve_ttf(fontfile):
	return send_from_directory(f'{STATIC_ROOT}/ttf', fontfile)


@app.route('/')
@app.route('/<path:file>')
def serve_file(file='index'):
	path = safe_join(FILES_ROOT, file)
	if not os.path.exists(path):
		return render_template('error404.jinja', title='404', path=file)
	with open(path, 'r', encoding='utf-8') as fp:
		basename = os.path.basename(path)
		return render_template('base.jinja', title=basename, body=fp.read(), clientip=remote_addr())
