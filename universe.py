import os
from sys import argv
from flask import Flask, send_from_directory, render_template, safe_join
app = Flask(__name__)

APP_ROOT = f'{os.path.dirname(__file__)}'
CSS_ROOT = APP_ROOT + '/css'
FILES_ROOT = APP_ROOT + '/files'

@app.route('/css/<path:stylesheet>')
def serve_css(stylesheet):
	return send_from_directory('css', stylesheet)

@app.route('/')
@app.route('/<path:file>')
def serve_file(file='index'):
	path = safe_join(FILES_ROOT, file)
	if not os.path.exists(path):
		return render_template('error404.jinja', title='404', path=path)
	with open(path, 'r', encoding='utf-8') as fp:
		return render_template('base.jinja', title=path, body=fp.read())
