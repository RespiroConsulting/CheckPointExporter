from prometheus_client import make_wsgi_app, Gauge
from wsgiref.simple_server import make_server
import os, subprocess

services = ['checkpoint_current_remote_users_count']

host = os.uname()[1]
g = Gauge('checkpoint_current_remote_users_count', 'Check users of checkpoint', ['host','script_name_pattern'])

def generate():
    for s in services:
        try:
            proc1 = subprocess.Popen(['ps', '-ef'], stdout=subprocess.PIPE)
            proc2 = subprocess.Popen(['grep', s], stdin=proc1.stdout,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            proc3 = subprocess.Popen(['wc', '-l'], stdin=proc2.stdout,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            proc1.stdout.close() # Allow proc1 to receive a SIGPIPE if proc2 exits.
            proc2.stdout.close() # Allow proc2 to receive a SIGPIPE if proc3 exits.