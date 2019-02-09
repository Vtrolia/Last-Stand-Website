function passwordEntered() {
        var password = document.getElementById("new");
        var button = document.querySelector("button");
        var oldTip = document.getElementById("newPassword");
        var NewTip = document.getElementById("passRepeat");
        closeToolTip(NewTip);
       
        
        if (password.value === document.getElementById("old").value) {
            password.style.backgroundColor = "#f72626";
            displayToolTip(oldTip, "Your new password cannot be the same as the old one!");
            oldTip.style.top = "42%";
            button.disabled = true;
            return;
        }
        
        else if (password.value != document.getElementById("new-repeat").value) {
            closeToolTip(oldTip);
            displayToolTip(NewTip, "Password and confirmation do not match!");
            password.style.backgroundColor = "white";
            button.disabled = true;
            return;
        }
        
        closeToolTip(oldTip);
        password.style.backgroundColor = "white";
        
        var upper = /[A-Z]/.test(password.value);
        var lower = /[a-z]/.test(password.value);
        var number = /[0-9]/.test(password.value);
        
        if (upper && lower && number && password.value.length >= 8) {
            closeToolTip(oldTip);
            
            document.getElementById("passwordForm").onkeypress = (e) => {
                if (e.keyCode === 13) {
                    submit();
                }
            }
            
            button.disabled = false;
            return;
        }
        
        else if (password.value.length > 0 && 
            password.value.length < 8) {
            displayToolTip(oldTip, "Your password is not complex enough or long enough!");
            oldTip.style.top = "35%";
            return;
        }
}

function sameTest() {
    var pass = document.getElementById("new").value;
    var passRepeat = document.getElementById("new-repeat");

    if (passRepeat.value != pass) {
        passRepeat.style.backgroundColor = "#f72626";
    }
    else {
        passRepeat.style.backgroundColor = "white";
    }
}

function closeToolTip(tip) {
    tip.style.visibility = "hidden";
    tip.style.opacity = 0;
}

function displayToolTip(tip, message) {
    tip.innerHTML = message;
    tip.style.visibility = "visible";
    tip.style.opacity = 1;
}

function submit() {
    document.onkeypress = undefined;
    let alerts = document.getElementById("alerts");
    
    try{
        alerts.parentElement.removeChild(alerts);
    }
    catch{}
    
    var form = {
        "old_password": document.getElementById("old").value,
        "new_password": document.getElementById("new").value
    };
    
    var request = new XMLHttpRequest();
    request.open("POST", "submit-password-change");
    request.setRequestHeader("X-CSRFToken", token);
    request.onload = () => {
        let inputs = document.getElementById("inputs");
        inputs.innerHTML += request.responseText;
    }
    request.send(form['old_password'] + "&" + form["new_password"]);
    
}

function switcher() {
    var eyes = document.getElementById("reveal-hide");
    var inputs = document.querySelectorAll("input");
    
    if (eyes.getAttribute("data-name") === "reveal") {
        eyes.title = "hide your passwords";
        eyes.setAttribute("data-name", "hide");
        let image = eyes.querySelector("img");
        image.src = reveal;
        
        
        for (let i = 0; i < inputs.length; i++) {
            inputs.item(i).type = "text";
        }
        
    }
    
    else {
        eyes.title = "reveal your passwords";
        eyes.setAttribute("data-name", "reveal");
        let image = eyes.querySelector("img");
        image.src = hide;
        
        for (let i = 0; i < inputs.length; i++) {
            inputs.item(i).type = "password";
        }
    }
}