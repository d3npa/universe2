import os
import shlex
from sys import argv
from datetime import datetime
from subprocess import Popen, PIPE
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


def exec_cmd(cmd):
	process = Popen(shlex.split(cmd), stdout=PIPE, stderr=PIPE)
	stdout, stderr = process.communicate()
	return (stdout.decode('utf-8'), stderr.decode('utf-8'))


@app.route('/css/<path:stylesheet>')
def serve_css(stylesheet):
	return send_from_directory(f'{STATIC_ROOT}/css', stylesheet)


@app.route('/ttf/<path:fontfile>')
def serve_ttf(fontfile):
	return send_from_directory(f'{STATIC_ROOT}/ttf', fontfile)


def serve_directory(dirpath):
	if not os.path.exists(dirpath):
		return ''
	if not os.path.isdir(dirpath):
		return serve_file(dirpath)
	html = ''
	os.chdir(dirpath)
	for f in os.listdir(dirpath):
		line, _ = exec_cmd(f'ls -l {f}')
		html += f'<a href="./{f}">{line} -></a>'
	os.chdir('..')
	return render_template(
		'base.jinja',
		title=dirpath, 
		body=html, 
		client_ip=remote_addr(),
		url_up=url_up(),
		)


def url_up():
	path = request.path
	if path[-1] == '/':
		path = path[:-1]
	return '/'.join(path.split('/')[:-1]) or '/'


@app.route('/')
@app.route('/<path:file>')
def serve_file(file='index'):
	path = safe_join(FILES_ROOT, file)
	if not os.path.exists(path):
		return render_template('error404.jinja', title='404', path=file)
	if os.path.isdir(path):
		return serve_directory(path)
	else:
		with open(path, 'r', encoding='utf-8') as fp:
			basename = os.path.basename(path)
			return render_template(
				'base.jinja',
				title=basename, 
				body=fp.read(), 
				client_ip=remote_addr(),
				url_up=url_up(),
				)
