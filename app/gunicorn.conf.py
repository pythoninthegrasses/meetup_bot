import os

workers = int(os.environ.get("WEB_CONCURRENCY", 1))
threads = 2
bind = "0.0.0.0:3000"
accesslog = "-"
