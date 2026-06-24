#!/bin/bash
# Gunicorn configuration file

import multiprocessing
import os

# Number of worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 60

# Server socket
bind = "0.0.0.0:8000"
backlog = 2048

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = "goshort"

# Server hooks
def post_fork(server, worker):
    """Called just after a worker has been forked."""
    pass

def pre_fork(server, worker):
    """Called just prior to forking the worker subprocess."""
    pass

def pre_exec(server):
    """Called just prior to exec() the new gunicorn master process."""
    pass

def when_ready(server):
    """Called just after the server is started."""
    print("Gunicorn server is ready. Spawning workers")

def worker_int(worker):
    """Called just after a worker exited due to a signal."""
    print(f"Worker {worker.pid} received interrupt signal")

def worker_abort(worker):
    """Called when a worker receives an SIGABRT signal."""
    print(f"Worker {worker.pid} received abort signal")
