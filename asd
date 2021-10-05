[fcgi-program:apteki]
# TCP socket used by Nginx backend upstream
socket=tcp://147.182.164.115:8002

# Directory where your site's project files are located
directory=/apteki/app

# Each process needs to have a separate socket file, so we use process_num
# Make sure to update "mysite.asgi" to match your project name
command=/apteki/venv/bin/daphne -u /apteki/run/apteki%(process_num)d.sock --fd 0 --access-log - --proxy-headers apteki.asgi:application

# Number of processes to startup, roughly the number of CPUs you have
numprocs=4

# Give each process a unique name so they can be told apart
process_name=asgi%(process_num)d

# Automatically start and recover processes
autostart=true
autorestart=true

# Choose where you want your log to go
stdout_logfile=/apteki/logs/asgi.log
redirect_stderr=true
