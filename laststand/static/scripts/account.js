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
        cloudCount.textContent = "clouds owned: ";
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
    var request = new XMLHttpRequest();
    request.open("GET", "password-reset-page");
    request.onload = () => {
        document.getElementById("settings-display").innerHTML = request.responseText;
    }
    request.send();

    if (!document.getElementById("passjs")) {
        var passjs = document.createElement("script");
        passjs.setAttribute("class", 'addOn');
        passjs.setAttribute("id", "passjs");
        passjs.setAttribute("src", static + "/password.js");
        document.querySelector("head").append(passjs);
    }
}

function deleteAccount() {
    var request = new XMLHttpRequest();
    request.open("GET", "delete-account");
    request.onload = () => {
        document.getElementById("settings-display").innerHTML = request.responseText;
    }
    request.send();

    if (!document.getElementById("deletejs")) {
        var deletejs = document.createElement("script");
        deletejs.setAttribute("id", "deletejs");
        deletejs.setAttribute("class", 'addOn');
        deletejs.setAttribute("src", static + "/delete.js");
        document.querySelector("head").append(deletejs);
    }
}

function becomePublisher() {
    var request = new XMLHttpRequest();
    request.open("GET", "become-publisher");
    request.onload = () => {
        document.getElementById("settings-display").innerHTML = request.responseText;
    }
    request.send();

    if (!document.getElementById("becomejs")) {
        var becomejs = document.createElement("script");
        becomejs.setAttribute("id", "becomejs");
        becomejs.className = "addOn";
        becomejs.setAttribute("src", static + "/become.js");
        document.querySelector("head").append(becomejs);
    }
}

function changeDetails() {
    var request = new XMLHttpRequest();
    request.open("GET", "change-details");
    request.onload = () => {
        document.getElementById("settings-display").innerHTML = request.responseText;
    }
    request.send();

    if (!document.getElementById("detailsjs")) {
        var detailsjs = document.createElement("script");
        detailsjs.setAttribute("id", "detailsjs");
        detailsjs.className = "addOn";
        detailsjs.setAttribute("src", static + "/details.js");
        document.querySelector("head").append(detailsjs);
    }
}