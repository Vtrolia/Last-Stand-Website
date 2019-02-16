var users = {};

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

function verify(which, toVerify) {
    usernames = Array.from(users[which]);
    if (usernames.includes(toVerify)) {
        var tip = document.createElement("div");
        tip.setAttribute("class", "tool-tip detail-tip");
        tip.setAttribute("id", "userTip");
        tip.style.visibility = "visible";
        tip.style.opacity = "1";
        tip.textContent = which.charAt(0).toUpperCase() + which.slice(1) + " already taken!";
        let user = document.getElementById("new-" + which);
        user.append(tip);
    }

    else {
        let del = document.getElementById("userTip");
        if (del) {
            del.parentElement.removeChild(del);
        }
    }
}

function change(type) {
    if (document.getElementById("alerts")) {
        let al = document.getElementById("alerts");
        al.parentElement.removeChild(al);
    }
    var toChange = {
        "change": String(type),
        "new": String(document.getElementById("new" + type).value),
        "password": document.getElementById("enter-password").value
    };
    
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