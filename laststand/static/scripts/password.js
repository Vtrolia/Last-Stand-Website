/*
 * For every time the user writes a character, check each input for validity, and 
 * enable the button if the input is valid, display a tooltip if it is not
 */
function passwordEntered() {
        var password = document.getElementById("new-password");
        var button = document.querySelector("button");
        var oldTip = document.getElementById("new-tip");
        var NewTip = document.getElementById("repeat-tip");
    
        // make sure no tooltip is showing at the beginning
        closeToolTip(NewTip);
       
        // tell the user that their old password can't be the same as their current
        if (password.value === document.getElementById("old-password").value) {
            password.style.backgroundColor = "#f72626";
            displayToolTip(oldTip, "Your new password cannot be the same as the old one!");
            oldTip.style.top = "42%";
            button.disabled = true;
            return;
        }
        
        // users have to verify their passwords
        else if (password.value != document.getElementById("new-repeat").value) {
            closeToolTip(oldTip);
            displayToolTip(NewTip, "Password and confirmation do not match!");
            password.style.backgroundColor = "white";
            button.disabled = true;
            return;
        }
        
        // if they get here, the fields are at least legal
        closeToolTip(oldTip);
        password.style.backgroundColor = "white";
        
    
        // a new password has to have an upper case letter, a lower case letter, and
        // a number. If the new password is legal, they can hit enter or click submit to submit
        var upper = /[A-Z]/.test(password.value);
        var lower = /[a-z]/.test(password.value);
        var number = /[0-9]/.test(password.value);
        
        if (upper && lower && number && password.value.length >= 8) {
            closeToolTip(oldTip);
            
            document.getElementById("password-form").onkeypress = (e) => {
                if (e.keyCode === 13) {
                    submit();
                }
            }
            
            button.disabled = false;
            return;
        }
        
        // else if password is not long enough
        else if (password.value.length > 0 && 
            password.value.length < 8) {
            displayToolTip(oldTip, "Your password is not complex enough or long enough!");
            oldTip.style.top = "35%";
            return;
        }
}

/*
 * Change the color of the input field based on the validity of the input
 */
function sameTest() {
    var pass = document.getElementById("new-password").value;
    var passRepeat = document.getElementById("new-repeat");

    if (passRepeat.value != pass) {
        passRepeat.style.backgroundColor = "#f72626";
    }
    else {
        passRepeat.style.backgroundColor = "white";
    }
}

// close tooltip passed in
function closeToolTip(tip) {
    tip.style.visibility = "hidden";
    tip.style.opacity = 0;
}

// set the message and the tooltip type and display it
function displayToolTip(tip, message) {
    tip.innerHTML = message;
    tip.style.visibility = "visible";
    tip.style.opacity = 1;
}

/*
 * Once the input is valid, the user is allowed to submit it, and based on whether or * not the server accepts this change, a message will be displayed at the bottom with * the server's reply
 */
function submit() {
    
    // delete the key listener and delete a previous alert if there is already one 
    document.onkeypress = undefined;
    let alerts = document.getElementById("alerts");
    
    try{
        alerts.parentElement.removeChild(alerts);
    }
    catch{}
    
    var form = {
        "old_password": document.getElementById("old-password").value,
        "new_password": document.getElementById("new-password").value
    };
    
    // submit the change request as a POST HTTP request, then display server's response
    var request = new XMLHttpRequest();
    request.open("POST", "submit-password-change");
    request.setRequestHeader("X-CSRFToken", token);
    request.onload = () => {
        let inputs = document.getElementById("inputs");
        inputs.innerHTML += request.responseText;
    }
    request.send(form['old_password'] + "&" + form["new_password"]);
    
}

/*
 * For ease of use, the password fields are able to be made visible on the screen.
 * The user will click the eye logo to change between the two 
 */
function switcher() {
    var eyes = document.getElementById("reveal-hide");
    var inputs = document.querySelectorAll("input");
    
    // reveal passwords if they are hidden
    if (eyes.getAttribute("data-name") === "reveal") {
        eyes.title = "hide your passwords";
        eyes.setAttribute("data-name", "hide");
        let image = eyes.querySelector("img");
        image.src = reveal;
        
        
        for (let i = 0; i < inputs.length; i++) {
            inputs.item(i).type = "text";
        }
        
    }
    
    // hide passwords if they are showing
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