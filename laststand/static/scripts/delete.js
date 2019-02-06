window.oninput = () => {
    var inputs = document.querySelectorAll("input");
    if (inputs.item(0).checked && inputs.item(1).value.length > 7) {
            document.getElementById("delete").disabled = false;
    }
}

function deleteAccount() {
    var request = new XMLHttpRequest();
    request.open("POST", "submit-delete-account");
    request.send("{\"password\": " + document.getElementById("deletePassword").value + ";}")
}
