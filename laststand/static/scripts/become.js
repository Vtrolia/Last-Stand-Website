window.oninput = () => {
    var text = document.querySelector("textarea");
    var ex = document.getElementById("example");
    
    if (ex.value && text.value) {
        document.getElementById("submit-publisher").disabled = false;
    }
}