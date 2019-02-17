var users = {};

/*
 * This function asks the api of the website for all the usernames and user emails so
 * that the user won't be able to change either to one that is already taken. Sent as
 * a JSON object
 */
function getUsers() {
    var request = new XMLHttpRequest();
    request.open("GET", "api/verify");
    request.setRequestHeader("X-CSRFToken", token);
    request.onload = () => {
        users = JSON.parse(request.responseText);
    }
    request.send();
}
getUsers();

/*
 * If the password is at least legal, they can submit. This does not check if the
 * password entered is the same as the one that was typed
 */
function enableButtons() {
    var password = document.getElementById("enter-password");
    if (password.value.length > 7) {
        var buttons = document.querySelectorAll("button");
        for (let i = 0; i < buttons.length; i++) {
            buttons.item(i).disabled = false;
        }
        
        document.getElementById("enter-password").oninput = undefined;
    }
}

/*
 * Makes sure the user is not entering an email or password that is already in use
 */
function verify(which, toVerify) {
    usernames = Array.from(users[which]);
    
    // if the username is already taken, warn the user
    if (usernames.includes(toVerify)) {
        var tip = document.createElement("div");
        tip.setAttribute("class", "tool-tip detail-tip");
        tip.setAttribute("id", "user-tip");
        tip.style.visibility = "visible";
        tip.style.opacity = "1";
        tip.textContent = which.charAt(0).toUpperCase() + which.slice(1) + " already taken!";
        let user = document.getElementById("new-" + which);
        user.append(tip);
    }
    
    // else, delete a tool-tip if it is present
    else {
        let del = document.getElementById("user-tip");
        if (del) {
            del.parentElement.removeChild(del);
        }
    }
}

/*
 * When the user has entered valid inputs, and they click the button to change 
 * a detail, this attempts to change that detail and gives the user the server's response
 */
function change(type) {
    
    // remove an alert if it already exitsts
    if (document.getElementById("alerts")) {
        let al = document.getElementById("alerts");
        al.parentElement.removeChild(al);
    }
    
    // JSON object to send to the server
    var toChange = {
        "change": String(type),
        "new": String(document.getElementById("new" + type).value),
        "password": document.getElementById("enter-password").value
    };
    
    // hopefully the user's input is valid and their changes can be made!
    var request = new XMLHttpRequest();
    request.open("POST", "/submit-details");
    request.setRequestHeader("X-CSRFToken", token);
    request.setRequestHeader("Content-type", "application/json");
    
    request.onload = () => {
        var response = JSON.parse(request.responseText);
        var alert = document.createElement("div");
        
        alert.setAttribute("id", "alerts");
        alert.setAttribute("class", "alert alert-" + response["flag"]);
        alert.innerHTML = response["body"];
        
        document.getElementById("change-details").append(alert);
        
    }
    request.send(JSON.stringify(toChange));
}