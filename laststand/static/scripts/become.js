function textStroke() {
    var text = document.querySelector("textarea");
    var ex = document.getElementById("example");
    
    if (ex.value && text.value) {
        document.getElementById("submit-publisher").disabled = false;
    }
}

window.addEventListener("submit", () => {
    if (document.getElementById("becomePublisher")) {
        alert("Your application was successfully received!");
    }
});