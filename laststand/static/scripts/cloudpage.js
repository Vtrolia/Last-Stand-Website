/*
 * gives automatic OS detection for the user's system so that they download the correct
 * version of the software for themselves
 */
  function loadOS() {
    // userAgent stores the user's operating system details
    var os = navigator.userAgent.split(/[()]+/)[1];

    // for Mac users
    if (os.includes("Mac")) {
        os = "macOS"

    }

    // else display the linux download
    else if (os.includes("Linux")){
        os = "Linux";
    }
	
    // FreeBSD coming soon
    else if (os.includes("BSD")) {
	os = "FreeBSD";
    }

    else {
	os = "none";
    }

    document.getElementById("hidden-os-type").value = os;
}

loadOS();
/*
 * When a user first selects to delete a cloud, prompt them to enter their password again for security reasons. 
 * Making any changes to their account should first require reauthentication 
 */
function displayPasswordPrompt() {
    
    // make the radio button text more responsive
    document.getElementById("yes-remove").style.color = "black";
    document.getElementById("delete-cloud-confirmation").style.display = "inline-block";
    
    // now, the button to submit a cloud deletion is disabled by default, again preventing the user from a
    // hasty deletion until the password seems like the right one, then they are allowed to submit
    document.getElementById("delete-cloud-password").oninput = () => {
        var input = document.getElementById("delete-cloud-password").value;
        var button = document.getElementById("enter-delete-cloud");
        
        if (input.length > 7) {
            button.disabled = false;
        }
        else {
            button.disabled = true;
        }
    }
}


/*
 * Once the user is authenticated, now they can delete the selected cloud. Sends a request back to the server
 * and will display a message to the user based on the result of the attempted deletion
 */
function deleteThisCloud() {
    
    // delete a previous alert if they tried before
    var alert = document.getElementById("alerts");
    if (alert) {
        alert.parentNode.removeChild(alert);
    }
    var name = document.getElementById("cloud-name").getAttribute("data-cloud");
    var password = document.getElementById("delete-cloud-password").value;
    
    // send a JSON object back to the server with the name of the User's cloud and their
    // password to be authenticated then deleted
    var request = new XMLHttpRequest();
    var data = {
        "name": name,
        "password": password,
    };
    
    request.open("POST", "/api/delete-cloud");
    request.setRequestHeader("X-CSRFToken", token);
    request.setRequestHeader("Content-type", "application/json");
    
    request.onload = () => {
        var response = JSON.parse(request.responseText);
        var alert = document.createElement("div");
        
        // create an alert div to tell the user what happened
        alert.setAttribute("id", "alerts");
        alert.setAttribute("class", "alert alert-" + response["flag"] + " cloud-alert");
        alert.innerHTML = response["body"];
        
        document.getElementById("cloud-page").append(alert);
        
        // remove the cloud that was just deleted from the display
        var cloud = document.getElementById("cloud-options");
        var clouds = cloud.querySelectorAll("li");

        if (response["flag"] === 'success') {
            for (let i = 0; i < clouds.length; i++)
            {
                 if (clouds.item(i).getAttribute("data-name") === name)
                 {
                     clouds.item(i).parentNode.removeChild(clouds.item(i));        
                 }
            }
       }
        
    }
    request.send(JSON.stringify(data));  
}