window.oninput = () => {
        var password = document.getElementById("new");
        var button = document.querySelector("button");
        var oldTip = document.getElementById("newPassword");
        var NewTip = document.getElementById("passRepeat");
        closeToolTip(NewTip);
        
        if (password.value === document.getElementById("old").value) {
            password.style.backgroundColor = "#f72626";
            displayToolTip(oldTip, "Your new password cannot be the same as the old one");
            button.disabled = true;
            return;
        }
        
        else if (password.value != document.getElementById("new-repeat").value || 
            password.length < 8) {
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
        
        if (upper && lower && number) {
            closeToolTip(oldTip);
            button.disabled = false;
            return;
        }
        
        else if (password.value.length > 0) {
            displayToolTip(oldTip, "Your password is missing either: <ul><li>An uppercase letter</li><li>A lowercase letter</li><li>Or a number</li></u>");
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