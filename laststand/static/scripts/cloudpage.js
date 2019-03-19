function displayPasswordPrompt() {
    document.getElementById("yes-remove").style.color = "black";
    document.getElementById("delete-cloud-confirmation").style.display = "inline-block";
    
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

function deleteThisCloud() {
    var alert = document.getElementById("alerts");
    if (alert) {
        alert.parentNode.removeChild(alert);
    }
    var name = document.getElementById("cloud-name").getAttribute("data-cloud");
    var password = document.getElementById("delete-cloud-password").value;
    
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
        
        alert.setAttribute("id", "alerts");
        alert.setAttribute("class", "alert alert-" + response["flag"] + " cloud-alert");
        alert.innerHTML = response["body"];
        
        document.getElementById("cloud-page").append(alert);
    }
    
    request.send(JSON.stringify(data));
    
    
}