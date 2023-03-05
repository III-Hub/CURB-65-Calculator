# RSE Assessment: CURB-65 Calculator 
# By Israel I Iwanga

## Install
**SQLite3 should be Installed on machine**

### local
1. **pip install fastapi**
2. **pip install uvicorn**
3. **pip install sqlalchemy**

### env
1. **pip install pipenv**
2. **pipenv shell**
3. **pipenv install**

**Type exit to leave env**

## To run app
**uvicorn books:app --reload**

**the app runs on 127.0.0.1:8000**

## To run test
1. **pytest**

## Deploy on linux server
**SQLite3 should be Installed on server**
**Copy the project on the server and cd in the directory**

1. **pip install fastapi uvicorn gunicorn**
2. **pip freeze > requirements.txt**
3. **pip install -r requirements.txt**

### Run the app
1. **gunicorn app:app -k uvicorn.workers.UvicornWorker**

**the app is running on 127.0.0.1:8000**

### Set up service
1. **sudo nano gunicorn_conf.py**

**Past the following code into gunicorn_conf.py**

```
# gunicorn_conf.py
from multiprocessing import cpu_count

bind = "127.0.0.1:8000"

# Worker Options
workers = cpu_count() + 1
worker_class = 'uvicorn.workers.UvicornWorker'

# Logging Options
loglevel = 'debug'
accesslog = '/home/fastapi_example/access_log'
errorlog =  '/home/fastapi_example/error_log'
```

**save and exit then run the following**

2.**sudo nano /etc/systemd/system/fastapi_example.service**

**Past the following code then save and exit**

```
[Unit]

Description=Gunicorn Daemon for FastAPI example

After=network.target


[Service]

User=ubuntu

Group=www-data

WorkingDirectory=/home/fastapi_example

ExecStart=/home/fastapi_example/env/bin/gunicorn -c gunicorn_conf.py main:app


[Install]

WantedBy=multi-user.target
```

**Set to auto restart**
3.**sudo systemctl start fastapi_example**
4.**sudo systemctl enable fastapi_example**

### Instal and setup NGINX
1.**sudo apt install nginx**
2.**sudo systemctl start nginx**
3.**sudo systemctl enable nginx**
4.**sudo nano /etc/nginx/sites-available/api.slingacademy.com**

**Past the following code then save and exit**

```
server {
        client_max_body_size 64M;
        listen 80;
        server_name api.slingacademy.com;

        location / {
                proxy_pass             http://127.0.0.1:8000;
                proxy_read_timeout     60;
                proxy_connect_timeout  60;
                proxy_redirect         off;

                # Allow the use of websockets
                proxy_http_version 1.1;
                proxy_set_header Upgrade $http_upgrade;
                proxy_set_header Connection 'upgrade';
                proxy_set_header Host $host;
                proxy_cache_bypass $http_upgrade;
        }

}
```

**enable the configuration file**

5. **sudo ln -s /etc/nginx/sites-available/api.slingacademy.com /etc/nginx/sites-enabled/**
6. **sudo systemctl restart nginx**

**The app is now accessible on server IP**