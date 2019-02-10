function findSelected(pressed) {
    document.getElementById("selectButton").disabled = false;
    var buttons = document.querySelectorAll(".radio_button");
    var current = pressed.querySelector("input");

    for (let i = 0; i < buttons.length; i++) {
        if (buttons.item(i) == current) {
            buttons.item(i).checked = true;
        }
        else {
            buttons.item(i).checked = false;
        }
    }
}
            
function selectPlan() {
    var items = {
        "plan": undefined,
    }
    var options = document.querySelectorAll(".radio_button");
    for (let i = 0; i < options.length; i++) {
        if (options.item(i).checked = true) {
            items["plan"] = options.item(i).getAttribute("data-name");
            break;
        }
    }

    var request = new XMLHttpRequest();
    request.open("POST", "/buy-plan");
    request.setRequestHeader("Content-Type", "application/json");
    request.send(JSON.stringify(items));
    request.onload = () => {
        if (request.responseText === "register") {
            alert("You have to sign in or create an account to purchase a plan!");
        }
        console.log(request.responseText);
        window.location.replace("/" + request.responseText);
    }

}