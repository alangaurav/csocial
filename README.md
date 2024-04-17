These are the setup instructions to get the server up and running for the Djnago project. 

This stack uses a combination of Nginx, Gunicorn, Daphne and Django for the full stack.
If you are on the development branch you can run the following command from the root priject directory for a test server

```
$ python3 manage.py runserver
```

Step 1: Requirements
Please install the following packages

```
$ pip3 install python-dotenv
$ pip3 install django
$ pip3 install django-extensions
$ pip3 install Pillow
$ python3 -m pip install gunicorn
$ python3 -m pip install daphne
```

Step 2: Setup env variables
In the root project directory create a .env file and set the follow variables.
The allowed hosts should hold the IP:Port and/or domain that Django will be listening to. 
The django secret key should be replaced with a valid secret key that you generate. 

```
#.env

DJANGO_SECRET_KEY='django-insecure-_m528p02+se^59ua^s1b^hwp*(q7@f*dc%vrz-a@o10oehjqs7'
DJANGO_DEBUG='True'
DJANGO_ALLOWED_HOSTS='127.0.0.1'
```

Step 3: Setup Gunicorn
There are two setup configs for gunicorn, developement and production. 
Each of these configs should be stored in /root_project/configs/gunicorn/
Ensure to set the variables based on your configuration. This includes setting the correct IP:Port for Gunicorn to communicate with both Django and Nginx.
You may need to create the following directories if they do not exist on your system:

1. /var/log/gunicorn
2. /var/run/gunicorn


```
#dev.py
#"""Gunicorn *development* config file"""
# Django WSGI application path in pattern MODULE_NAME:VARIABLE_NAME
wsgi_app = "csocials.wsgi:application"
# The granularity of Error log outputs
loglevel = "debug"
# The number of worker processes for handling requests
workers = 2
# The socket to bind
bind = "127.0.0.1:8000"
# Restart workers when code changes (development only!)
reload = True
# Write access and error info to /var/log
accesslog = errorlog = "/var/log/gunicorn/dev.log"
# Redirect stdout/stderr to log file
capture_output = True
# PID file so you can easily fetch process ID
pidfile = "/var/run/gunicorn/dev.pid"
# Daemonize the Gunicorn process (detach & enter background)
daemon = True
# Add graecful time out to restart workers in case they are killed
graceful_timeout = 120
```

```
#production.py
#"""Gunicorn *production* config file"""

import multiprocessing

# Django WSGI application path in pattern MODULE_NAME:VARIABLE_NAME
wsgi_app = "csocials.wsgi:application"
# The number of worker processes for handling requests
workers = multiprocessing.cpu_count() * 2 + 1
# The socket to bind
bind = "0.0.0.0:80"
# Write access and error info to /var/log
accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
# Redirect stdout/stderr to log file
capture_output = True
# PID file so you can easily fetch process ID
pidfile = "/var/run/gunicorn/prod.pid"
# Daemonize the Gunicorn process (detach & enter background)
daemon = True
# Add graecful time out to restart workers in case they are killed
graceful_timeout = 120
```

Once you create and save your Gunicorn config file you can run gunicorn using the following command from the root project directory:

```
$ gunicorn -c /config/gunicorn/dev.py
```

Step 4: Nginx setup 
With Gunicorn up and running you can now setup and run nginx to listen to clients on the ip or domain you have setup. 
Ensure you change the variables to your configuration of servers. 
Based on whether you are running a development or production server, you may choose your configuration. 
In case you are running a production server, please make sure you either have SSL/TSL certificates and variables set per the config, or comment these lines out. 

```
# Nginx "development" configuration
# /etc/nginx/sites-available/csocials-dev.conf

server_tokens               off;
access_log                  /var/log/nginx/csocials.access.log;
error_log                   /var/log/nginx/csocials.error.log;

# This configuration will be changed to redirect to HTTPS later
server {
  server_name               .csocials;
  listen                    80;
  location / {
    proxy_pass              http://localhost:8000;
    proxy_set_header        Host $host;
    proxy_set_header    X-Forwarded-Proto $scheme;
  }

  location /static {
          autoindex on;
          alias /path/to/root/directory/static/;
  }

  location /media {
          autoindex on;
          alias /path/to/root/directory/media/;
  }
}
```


```
# Nginx "production" configuration
# /etc/nginx/sites-available/csocials-prod.conf
# This file inherits from the http directive of /etc/nginx/nginx.conf

# Disable emitting nginx version in the "Server" response header field
server_tokens               off;

# Use site-specific access and error logs
access_log                  /var/log/nginx/csocials.access.log;
error_log                   /var/log/nginx/csocials.error.log;

# Return 444 status code & close connection if no Host header present
server {
  listen                  80 default_server;
  return                  444;
}

# Redirect HTTP to HTTPS
server {
  server_name             .csocials;
  listen                  80;
  return                  307 https://$host$request_uri;
}

server {

  # Pass on requests to Gunicorn listening at http://localhost:8000
  location / {
    proxy_pass              http://localhost:8000;
    proxy_set_header      Host $host;
    proxy_set_header      X-Forwarded-Proto $scheme;
    proxy_set_header      X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_redirect        off;
    client_max_body_size 20M; # The default limit is 1MB increase this for file uploads
  }

  # Serve static files directly
  location /static {
          autoindex on;
          alias /path/to/root/directory/static/;
  }

  # Serve media files directly
  location /media {
          autoindex on;
          alias /path/to/root/directory/media/;
  }

  listen 443 ssl;
  # These are all SSL and TSL certificate variables that need to be set. Syntax var val;
  #ssl_certificate 
  #ssl_certificate_key
  #include conf
  #ssl_dhparam 
}
```

Once you have created these files in /etc/nginx/sites-available/ you need to link them to /etc/nginx/sites-enabled/ for them to be used. You can do so using the following commands:
```
$ cd /etc/nginx/sites-enabled
$ sudo ln -s ../sites-available/csocials-production .
```

Step 5: Bring it all together
With all the above files saved and configuration you will now be able to run your server.
To get the server up and running follow these steps:

1. In your root project directory run
```
$ python3 manage.py collectstatic
```
This will allow you to collect all your static files into the /static directory for production. 
2. Start gunicorn, run the following commands in the root project directory:
```
$ gunicorn -c config/gunicorn/production.py
```
3. Start Nginx using the following command:
```
$ sudo systemctl start nginx
```
You can now access your website using the domain or ip you have specified in the configs. Please remember when using Nginx you access only the ip, do not include the port as part of the url. 

To access the logs simply use :
```
$ tail /var/log/path/to/log/file
``` 
