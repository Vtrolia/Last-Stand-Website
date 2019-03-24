var os;
        
        function makeName(option) {
            os = option.getAttribute("data-os");
            document.getElementById("first-options").style.display = "none";
            document.getElementById("cloud-name").style.display = "inherit";
            document.getElementById("os-type").setAttribute("value", os);
            
        }
        
        function userMessage() {
            document.getElementById("cloud-name").style.display = "none";
            document.getElementById("cloud-download").style.display = "inherit";
        }
        
        function backToStart(div) {
            document.getElementById(div).style.display = "none";
            document.getElementById("first-options").style.display = "inherit";
        }
        
       
       /*
        * To protect the user from themselves, they are not allowed to create two clouds with the same name,
        * this function grabs all of the user's clouds from the api and then makes sure that the text input watches for duplicates
        */
       window.onload = () => {
           var resp;
           
           // requires csrf protection
           var request = new XMLHttpRequest();
           request.open("GET", "api/get-user-clouds");
           request.setRequestHeader("X-CSRFToken", token);
           request.onload = () => {
               resp = JSON.parse(request.responseText);
               
               // when the user is typing their cloud, if the value matches another cloud they are given ample warning
               // (dont worry, the server prevents it if the user thinks they're being slick)
               document.getElementById("new-cloud-name").oninput= () => {
                   var name = document.getElementById("new-cloud-name");

                   for(let cloud in resp) {
                       if (name.value === cloud) {
                           
                           // give them multiple warnings and disable the button
                           document.querySelector("button").disabled = true;
                           alert("More than one cloud cannot have the same name!");
                           name.style.backgroundColor = "red";
                           return;
                       }
                   }
                   document.querySelector("button").disabled = false;
                   name.style.backgroundColor = "white";
               }
           }
           request.send()
       }