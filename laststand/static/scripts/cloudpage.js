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