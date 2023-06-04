## Running server application and tests
---
0. Preparation, install localy: `python3`, `python3-pip`, `python3-venv`
1. Build virual enviroment in folder `MyParkingSpace`: `python3 -m venv venv`
2. Source enviroment: `source ./venv/bin/activate` (linux) `./venv/Scripts/activate` (windows)
3. Install project: `pip3 install -e .`
4. Install dependencies: `pip3 install -r Server/requirements.txt`
4. Go to folder `Server` and type: 
    - for run tests: `python3 BackendSystemTests`
    - for run app: `python3 Backend`

### Supported Backend flags
---
```
--ipaddress <address>
--logfilepath <path>
--loglevel <DEBUG/INFO/ERROR>
--databasepath <path>
--newdatabase
```

### Supported BackendSystemTests flags
---
```
--testcase <testcase simple regex>
--loglevel <DEBUG/INFO/ERROR>
--os <linux/windows/ci-linux>
```