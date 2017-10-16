# keras-sacred
Run sacred with keras on local machine and on your server

## Preparation

- Install mongodb: `apt-get install mongodb`
- Install sacred: `pip install sacred`
- Install sacredboard locally (on Python 3 environment): `pip install https://github.com/chovanecm/sacredboard/archive/develop.zip`

## Set up your mongodb

- Create the following directory structure wherever you want:
```
mkdir MongoDB
mkdir MongoDB/db MongoDB/Log
```

- Create the mongodb configuration file:
```
# mongod.conf

# Where and how to store data.
storage:
  dbPath: <path-to>/MongoDB/db
  journal:
    enabled: true

# where to write logging data.
systemLog:
  destination: file
  logAppend: true
  path: <path-to>/MongoDB/Log/mongod.log

# network interfaces
net:
  port: 27017
  bindIp: 127.0.0.1
```

**Note:** If you are running this on the server just comment out the `bindIp` line. Also, if the port is taken use 27018 etc.

- Start the mongodb daemon:

`mongod --config <path-to>/MongoDB/mongod.conf`

## Setup your keras script

- Set up sacred to run with your keras script like the example given

## Run sacredboard and watch your experiments

- For local experiments: `sacredboard -m <db-name>`
- For monitoring server experiments: `sacredboard -m <server-static-ip>:<port>:<db-name>`
