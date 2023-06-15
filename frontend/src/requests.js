import { fetch as requestToServer } from 'whatwg-fetch';
import { logMessage } from './Logger';

export async function sendRequestForLoginToServer(login, password) {

    return await requestToServer('/api/login',
        {
            body: JSON.stringify({
                "Login": login,
                "Password": password
            }),
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept',
            },
            mode: 'no-cors',
            method: 'POST',
            redirect: 'follow'
        }
    )
        .then(function (response) {
            return response.json();
        })
        .then(function (myJson) {
            if (myJson["error"]) {
                logMessage("error", myJson["error"]);
            }
            else if (myJson["token"]) {
                logMessage("success", "Login user: " + login);
                return myJson["token"];
            }
        });
}

export async function sendRequestForRegisterToServer(login, password, email, name) {

    return await requestToServer('/api/register',
        {
            body: JSON.stringify({
                "Login": login,
                "Password": password,
                "Email" : email,
                "Name" : name
            }),
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept',
            },
            mode: 'no-cors',
            method: 'POST',
            redirect: 'follow'
        }
    )
        .then(function (response) {
            console.log("DEBUG LOGS: ", response)
            return response.json();
        })
        .then(function (myJson) {
            if (myJson["error"]) {
                logMessage("error", myJson["error"]);
                return false;
            }
            else {
                logMessage("success", "Registered user: " + login);
                return true;
            }
        });
}

export async function sendRequestForLogoutToServer(token) {

    return await requestToServer('/api/logout',
        {
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept',
                'Authorization': "token " + token,
            },
            mode: 'no-cors',
            method: 'POST',
            redirect: 'follow'
        }
    )
        .then(function (response) {
            return response.json();
        })
        .then(function (myJson) {
            if (myJson["error"]) {
                logMessage("error", myJson["error"]);
                return false;
            }
            else {
                logMessage("success", "Logout user!");
                return true;
            }
        });
}

export async function sendRequestForParkingSlotsByDateToServer(token, date) {

    return await requestToServer('/api/parking/slots/' + date,
        {
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept',
                'Authorization': "token " + token,
            },
            mode: 'no-cors',
            method: 'POST',
            redirect: 'follow'
        }
    )
        .then(function (response) {
            return response.json();
        })
        .then(function (myJson) {
            if (myJson["error"]) {
                logMessage("error", myJson["error"]);
            }
            else {
                return myJson["slots"]
            }
        });
}
