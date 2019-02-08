window.oninput = () => {
    if (!document.getElementById("becomePublisher")) {
        return false;
    }
    
    var text = document.querySelector("textarea");
    var ex = document.getElementById("example");
    
    if (ex.value && text.value) {
        document.getElementById("submit-publisher").disabled = false;
    }
}

document.getElementById("submit-publisher").addEventListener("submit", () => {
    alert("Your application was successfully received!");
})