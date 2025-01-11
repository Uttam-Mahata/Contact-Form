# Gunicorn configuration file

# Python version
python_version = "3.11"

# Server socket
bind = "0.0.0.0:8000"  # IP and port to bind
backlog = 2048         # Maximum number of pending connections

# Worker processes
workers = 3            # Number of worker processes (2-4 x NUM_CORES recommended)
worker_class = "sync"  # Type of worker (sync, gevent, etc.)
worker_connections = 1000
timeout = 60           # Worker timeout in seconds
keepalive = 2         # Keepalive timeout

# Process naming
proc_name = "contact_form"
pythonpath = "."

# Logging
accesslog = "logs/access.log"
errorlog = "logs/error.log"
loglevel = "info"

# SSL (uncomment if using HTTPS)
# keyfile = "/path/to/keyfile"
# certfile = "/path/to/certfile"

# Server mechanics
daemon = False         # Don't run in background
user = None           # Process owner
group = None          # Process group

# Server hooks
pre_fork = None
post_fork = None
pre_exec = None
pre_request = None
post_request = None
worker_exit = None

# Application
wsgi_app = "app:app"  # Format is "module_name:application_name"