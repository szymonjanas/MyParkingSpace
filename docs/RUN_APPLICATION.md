# Build and run backend application (flask) and tests
---
0. Preparation, install localy: `python3, python3-pip, python3-venv`
1. Build and use virtual enviroment in folder `MyParkingSpace`:
    ```sh
    python3 -m venv venv
    source ./venv/bin/activate # linux 
    ./venv/Scripts/activate # windows
    ```
3. Install project and dependencies: 
    ```sh
    pip3 install -e .
    pip3 install -r Server/requirements.txt
    ```
4. Go to folder `Server` and type: 
    ```sh
    python3 BackendSystemTests # run tests
    python3 Backend # run app
    ```
    
### Supported Backend flags
---
```sh
--ipaddress <address> # without port, fixed port: 5566
--logfilepath <path>
--loglevel <DEBUG/INFO/ERROR>
--databasepath <path>
--newdatabase # WARNING! Will erase old database!
--emailaddress <address>
--emailpassword <password>
--emailconfig # get email setting from config.json
--testmode #turn on TEST_MODE - sends email to same sender address
```

### Supported BackendSystemTests flags
---
```sh
--testcase <testcase simple regex> # --testcase qrcode
--loglevel <DEBUG/INFO/ERROR> # DEBUG is routing real time logs from application to testcase logging
--os <linux/windows/ci-linux>
# Config email sender application auth:
--emailconfig # get email settings from config.json
--emailaddress <email>
--emailpassword <password>
```

# Build and run frontend (react) application
0. Preparation, install localy npm, node.js
1. Install dependencies
    ```sh
    cd /frontend
    npm install
    ```
2. A. Run application as separate:

    Server IP address has to match address in `/frontend/package.json`
    ```sh
    npm start
    ```

2. B. Run application with Server as one:

    ```sh
    npm run build
    ```
    and then run Server. Make sure to maintain directory order, as Frontend is taken with a path `../frontend/build` at Server
