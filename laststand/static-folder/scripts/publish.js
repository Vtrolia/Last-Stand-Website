window.onkeydown = () => { 
        if (document.getElementById("title").value && document.getElementById("content").value) {
            if (document.getElementById("file").value) {
                if (document.getElementById("credit").value) {
                    document.getElementById("subber").disabled = false;
                }
                else {
                    document.getElementById("subber").disabled = true;
                }
            }
            
            document.getElementById("subber").disabled = false;
        }
    }
    
    function falser() {
        document.getElementById("subber").disabled = true;
    }
    
    function displayModal() {
        var modal = document.getElementById("style-guide-box");
        modal.style.display = 'block';
        document.addEventListener("click", (e) => {
            if (e.target.getAttribute("id") === "style-guide-box") {
                modal.style.display = "none";
            }
        });
    }