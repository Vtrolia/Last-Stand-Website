window.oninput = () => {
    var inputs = document.querySelectorAll("input");
    if (inputs.item(0).checked && inputs.item(1).value.length > 7) {
            document.getElementById("delete").disabled = false;
    }
}

