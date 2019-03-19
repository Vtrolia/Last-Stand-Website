/*
 * User details and the details of their clouds have to be sent over from the 
 * dyanmically, so when the window first loads that information is retrieved and
 * put into the accoubt-details section
 */
window.onload = () => {
    // server sends the details as a JSON object
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

// get cloud options placeholder
function displayCloudOptions(cloud) {
    var request = new XMLHttpRequest();
    request.open("GET", "/cloud-options-page");
    request.onload = () => {
        let display = document.getElementById("settings-display");
        display.innerHTML = request.responseText;
        display.innerHTML += "<div id='cloud-name' style='display:hidden' data-cloud='" + cloud.getAttribute("data-name") + "'></div>"
        let form = document.getElementById("download-client-form");
        form.innerHTML += "<input type='hidden' value='" + cloud.getAttribute("data-name") + "' name='cloud-name' id='cloud-name-hidden'>"
        document.getElementById("settings-title").textContent = "Settings for " + cloud.getAttribute("data-name");
    }
    request.send(cloud.getAttribute("data-name"));
    
    loadScript("cloudpage");
}

// when user presses back-button or when the page loads for the first time, delete the 
// previous page's JS and show the base settings page
function getBaseSettings() {
    var request = new XMLHttpRequest();
    request.open("GET", "base-options-page");
    request.onload = () => {
        document.getElementById("settings-display").innerHTML = request.responseText;
    }
    request.send();
    
    // all JS files, when added to the document, are given the class "add-on", so that
    // they can be found and deleted
    var addOnJS = document.querySelectorAll(".add-on");
    for (let i = 0; i < addOnJS.length; i++) {
        addOnJS.item(i).parentElement.removeChild(addOnJS.item(i));
    }

}

// get cloud placeholder
function planChange() {
    var request = new XMLHttpRequest();
    request.open("GET", "change-plan-page");
    request.onload = () => {
        document.getElementById("settings-display").innerHTML = request.responseText;
        document.getElementById("settings-title").textContent = "Change your plan";
    }
    request.send();
}

// get reset screen
function passwordReset() {
    loadTemplate("password-page");
    loadScript("password");
}

// get delete screen
function deleteAccount() {
    loadTemplate("delete");
    loadScript("delete");
}

// get publisher screen
function becomePublisher() {
    var request = new XMLHttpRequest();
    request.open("GET", "become-publisher");
    request.onload = () => {
        document.getElementById("settings-display").innerHTML = request.responseText;
    }
    request.send();
    loadScript("become");
}

// get details screen
function changeDetails() {
    loadTemplate("change-details");
    loadScript("details");
}

/*
 * takes the template for the page being requested and loads it into settings-display
 */
function loadTemplate(template) {
    var request = new XMLHttpRequest();
    request.open("GET", "load/" + template);
    request.setRequestHeader("X-CSRFToken", token);
    request.onload = () => {
        document.getElementById("settings-display").innerHTML = request.responseText;
    }
    request.send();
}

/*
 * Find the script associated with the template being loaded and add it to the header
 * with the class "add-on"
 */
function loadScript(name) {
    if (!document.getElementById(name + "js")) {
        var jsfile = document.createElement("script");
        jsfile.setAttribute("id", name + "js");
        jsfile.className = "add-on";
        jsfile.setAttribute("src", static + "/" + name + ".js");
        document.querySelector("head").append(jsfile);
    }
}