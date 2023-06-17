import { fetch as requestToServer } from 'whatwg-fetch';
import { logMessage } from './Logger';


///////////////////////
// ADMISSION CONTROL //
///////////////////////
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

///////////////////////
// SPACE RESERVATION //
///////////////////////
export async function sendRequestForParkingSlotsByDate(token, date) {

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
            method: 'GET',
            redirect: 'follow'
        }
    )
        .then(function (response) {
            return response.json();
        })
        .then(function (myJson) {
            if (myJson["error"]) {
                logMessage("error", myJson["error"]);
                return { "slots" : [] }
            }
            else {
                return myJson["slots"]
            }
        });
}

export async function sendRequestForNewReservation(token, reservation) {

    return await requestToServer('/api/reservation/new',
        {
            body: JSON.stringify(reservation),
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept',
                'Authorization': "token " + token
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
                logMessage("success", "New reservation created!");
                return true;
            }
        });
}

export async function sendRequestForGetAllReservations(token) {

    return await requestToServer('/api/reservation/all',
        {
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept',
                'Authorization': "token " + token
            },
            mode: 'no-cors',
            method: 'GET',
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
                return myJson;
            }
        });
}

export async function sendRequestForGetAllParkingSlots(token) {

    return await requestToServer('/api/parking/slots/all',
        {
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept',
                'Authorization': "token " + token
            },
            mode: 'no-cors',
            method: 'GET',
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
                return myJson;
            }
        });
}

export async function sendRequestForDeleteReservation(token, reservationId) {

    return await requestToServer('/api/reservation/'+ reservationId,
        {
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept',
                'Authorization': "token " + token
            },
            mode: 'no-cors',
            method: 'DELETE',
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
                logMessage("success", "Reservation deleted!");
                return true;
            }
        });
}

export async function sendRequestForGetReservationQrCode(token, reservationId) {

    return await requestToServer('/api/reservation/qr/'+ reservationId,
        {
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'image/png',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept',
                'Authorization': "token " + token
            },
            mode: 'no-cors',
            method: 'GET',
            redirect: 'follow'
        }
    )
        .then(response => response.blob());
}

export async function sendRequestForUserInfo(token) {

    return await requestToServer('/api/user',
        {
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Origin, X-Requested-With, Content-Type, Accept',
                'Authorization': "token " + token
            },
            mode: 'no-cors',
            method: 'GET',
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
                return myJson["user"];
            }
        });
}
