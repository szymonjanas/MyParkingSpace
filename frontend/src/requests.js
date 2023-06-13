import { fetch as requestToServer } from 'whatwg-fetch';
import { logMessage } from './Logger';

export async function sendRequestForLoginToServer({ login, password }) {

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
            else if (myJson["jwt"]) {
                logMessage("success", "Login user: " + login);
                return myJson["jwt"];
            }
        });
}
