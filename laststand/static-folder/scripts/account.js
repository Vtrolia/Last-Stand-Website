window.onload = () => {
    var request = new XMLHttpRequest();
    request.open("POST", "/api/get-user-cloud-info");
    request.setRequestHeader("X-CSRFToken", token);
    request.onload = () => {
        let response = JSON.parse(request.responseText);

        let bold = document.createElement("strong");
        bold.textContent = response['status'];
        let status = document.getElementById("account-status");
        status.textContent = "You are a subscriber of the "
        status.appendChild(bold);
        status.innerHTML += " plan"

        let cloudCount = document.getElementById("clouds");
        cloudCount.textContent = "Clouds owned: ";
        let count = document.createElement("strong");
        count.textContent = response['clouds_owned'];
        cloudCount.appendChild(count);

        let cloudList = document.getElementById("cloud-options");
        for (let i = 0; i < response['clouds'].length; i++) {
            let cloud = document.createElement("li")
            cloud.textContent = response['clouds'][i];
            cloud.className = "cloud-option";
            cloud.setAttribute("data-name", cloud.textContent)
            cloud.setAttribute("onclick", "displayCloudOptions(this)")
            cloudList.appendChild(cloud);
        }
    }
    
    request.send();
    getBaseSettings();
}

function displayCloudOptions(cloud) {
    var request = new XMLHttpRequest();
    request.open("GET", "/cloud-options-page");
    request.onload = () => {
        let display = document.getElementById("settings-display");
        display.innerHTML = request.responseText;
        document.getElementById("settings-title").textContent = "Settings for " + cloud.getAttribute("data-name");
    }
    request.send(cloud.getAttribute("data-name"));
}

function getBaseSettings() {
    var request = new XMLHttpRequest();
    request.open("GET", "base-options-page");
    request.onload = () => {
        document.getElementById("settings-display").innerHTML = request.responseText;
    }
    request.send();

    var addOnJS = document.querySelectorAll(".addOn");
    for (let i = 0; i < addOnJS.length; i++) {
        addOnJS.item(i).parentElement.removeChild(addOnJS.item(i));
    }

}

function planChange() {
    var request = new XMLHttpRequest();
    request.open("GET", "change-plan-page");
    request.onload = () => {
        document.getElementById("settings-display").innerHTML = request.responseText;
        document.getElementById("settings-title").textContent = "Change your plan";
    }
    request.send();
}

function passwordReset() {
    loadTemplate("password-page");
    loadScript("password");
}

function deleteAccount() {
    loadTemplate("delete");
    loadScript("delete");
}

function becomePublisher() {
    var request = new XMLHttpRequest();
    request.open("GET", "become-publisher");
    request.onload = () => {
        document.getElementById("settings-display").innerHTML = request.responseText;
    }
    request.send();
    loadScript("become");
}

function changeDetails() {
    loadTemplate("change-details");
    loadScript("details");
}

function loadTemplate(template) {
    var request = new XMLHttpRequest();
    request.open("GET", "load/" + template);
    request.setRequestHeader("X-CSRFToken", token);
    request.onload = () => {
        document.getElementById("settings-display").innerHTML = request.responseText;
    }
    request.send();
}

function loadScript(name) {
    if (!document.getElementById(name + "js")) {
        var jsfile = document.createElement("script");
        jsfile.setAttribute("id", name + "js");
        jsfile.className = "addOn";
        jsfile.setAttribute("src", static + "/" + name + ".js");
        document.querySelector("head").append(jsfile);
    }
}