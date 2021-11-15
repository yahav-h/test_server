# test_server

---

This repository contains a simple RESTAful API server with one serving index.html

---

## Prerequisites:

1. Must have Python3.9.x Installed; If not, refer to https://python.org/downloads . 
2. Must have pip Installed; If not, refer to https://pip.pypa.io/en/stable/installing .
3. Once all 1&2 are installed and ready, You'll need to create a new virtual environment, use the below command from the PROJECT_DIRECTORY 
```shell
python3 -m venv ./venv
```
4. Install all dependencies by the following command from the PROJECT_DIRECTORY
```shell
python3 -m pip install -r ./requirements.txt
```
---

##  Compile:
Regardless what kind of operating system you run, 

Using the command below will deploy an executable to your machine.

Note that , compiling source code on Windows machine will produce a .exe which will not work on other machines (same apply for any type of machine)
```shell
pyinstaller --onfile server.py
```

---
## Server Running + Swagger:

+ The default PORT for this server is `8443`
+ Once binary server is running , navigate to http://locahost:8443 for interaction
+ While server is running, navigate to http://localhost:8443/docs from documentation

## Modules Info:

### `server.py`

+ Main Server Module, Contains all routing as well as Base64 of INDEX.HTML
+ Serves a `__main__` function to run serer as script

### `redis_interface.py`

+ A simple REDIS implementation, responsible for CRUD actions including DUMP of In-Memory to Storage  

### `helpers.py`

+ A Utility Module, Contains a Singleton Implementation and a PathUtil class
+ Note that PathUtil handle both Development mode as well Deployed (as binary) mode 

---

## Resources:

### `dump.rdb`
+ The `dump.rdb` resource responsible to store all In-Memory dumps to Storage and work as a Cache file

### `requirements.txt`
+ The `requirements.txt` resource contains all dependencies for this repository

### `deploy.sh` 
+ Simple `#!/bin/bash` script which compile the project for a Mac / Linux based environments 

### `deploy.bat`
+ Simple `batch` script which compile the project for a Windows based environments 