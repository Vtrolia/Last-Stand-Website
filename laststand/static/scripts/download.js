/*
 * gives automatic OS detection for the user's system so that they download the correct
 * version of the software for themselves
 */
window.onload = () => {
    // userAgent stores the user's operating system details
    var os = navigator.userAgent.split(/[()]+/)[1];
    os = os.split(" ")[0];

    // for Mac users
    if (os.includes("Mac")) {
        os = "macOS"

    }

    // their is no Windows version yet, so don't allow Windows users to download
    else if (os.includes("Windows")) {
        let buttons =  document.getElementById("download-buttons");
        buttons.parentElement.removeChild(buttons);

        let h3 = document.createElement("h3");
        h3.innerHTML = "Sorry! Windows isn't available yet! Make sure to check back in the future!";
        document.getElementById("first-downloads-page").appendChild(h3);
        return false;
    }

    // else display the linux download
    else {
        os = "Linux";
    }

    // when the form is sent to the server, make sure it is for the correct OS
    let labels = document.querySelectorAll("label");
    for(let i = 0; i < labels.length; i++) {
        labels.item(i).innerHTML += ": " + os;
    }

    document.getElementById("os-type").value = os;
}

// when user has agreed to the licensing agreement, they can download the software
function allow() {
     var buttons = document.querySelectorAll("button");
     for (let i = 0; i < buttons.length; i++){
         buttons.item(i).disabled = false;    
    }
 }