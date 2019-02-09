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
            tip.setAttribute("class", "toolTip");
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