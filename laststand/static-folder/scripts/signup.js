/*
 * When the user has entered all fields and agreed to the licensing agreement, they can 
 * create their account
 */
function enabler() {
    var button = document.getElementById("register-button");
    var entries = document.querySelectorAll("input");
    var box = document.getElementById("agree");
    var password = document.getElementById("signup-password");
    
    if (password.value.length < 8)
    {
         button.disabled = true;
        return false   
    }

    for (let i = 0; i < entries.length; i++) {
        if (!entries.item(i).value) {
            button.disabled = true;
            return false;
        }
    }

    if (box.checked) {
        button.disabled = false;
    }
    else {
        button.disabled = true;
    }

}
    
window.oninput = enabler;