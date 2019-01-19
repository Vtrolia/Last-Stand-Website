function enabler() {
        var button = document.getElementById("registerbutton");
        var entries = document.querySelectorAll("input");
        var box = document.getElementById("agree");
        
        for (let i = 0; i < entries.length; i++) {
            if (entries.item(i).value == "") {
                button.disabled = true;
                return false;
            }
        }
        
        if (box.checked) {
            button.disabled = false;
        }
        else {
            button.disabled = true;
        }
        
    }
    
    window.oninput = enabler;