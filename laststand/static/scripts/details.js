function enableButtons() {
    var password = document.getElementById("enter-password");
    if (password.value.length > 7) {
        var buttons = document.querySelectorAll("button");
        for (let i = 0; i < buttons.length; i++)
        {
            buttons.item(i).disabled = false;
        }
        
        document.getElementById("enter-password").oninput = undefined;
    }
}