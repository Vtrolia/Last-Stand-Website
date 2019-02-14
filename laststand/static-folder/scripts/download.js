 window.onload = () => {
        var os = navigator.userAgent.split(/[()]+/)[1];
        os = os.split(" ")[0];
        
        if (os.includes("Mac")) {
            os = "macOS"
            
        }
        
        else if (os.includes("Windows")) {
            let buttons =  document.getElementById("download-buttons");
            buttons.parentElement.removeChild(buttons);
            
            let h3 = document.createElement("h3");
            h3.innerHTML = "Sorry! Windows isn't available yet! Make sure to check back in the future!";
            document.getElementById("first-downloads-page").appendChild(h3);
            return false;
        }
     
        else {
            os = "Linux";
        }
        
        let labels = document.querySelectorAll("label");
        for(let i = 0; i < labels.length; i++) {
            labels.item(i).innerHTML += ": " + os;
        }
        
        document.getElementById("os-type").value = os;
    }
 
function allow() {
     var buttons = document.querySelectorAll("button");
     for (let i = 0; i < buttons.length; i++){
         buttons.item(i).disabled = false;    
    }
 }