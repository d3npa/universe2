import os
from universe import app as universe
from flup.server.fcgi import WSGIServer
from sys import argv

if __name__ == '__main__':
	socket_path = f'{os.path.dirname(argv[0]) or "."}/universe.sock'
	WSGIServer(universe, bindAddress = socket_path).run()
