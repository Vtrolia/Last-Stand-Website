/*
 * For every key press, check if all neccesary fields have input. The user does not have 
 * to enter an author credit if they are not adding an image to their article.
 */
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

// let user submit
function falser() {
    document.getElementById("subber").disabled = true;
}

/*
 * When a publisher wants to review the style guide, it shows as a popup in the middle 
 * of the screen in a box. This displays that box and a modal around it so it can be 
 * easily clicked off
 */
function displayModal() {
    var modal = document.getElementById("style-guide-box");
    modal.style.display = 'block';
    document.addEventListener("click", (e) => {
        if (e.target.getAttribute("id") === "style-guide-box") {
            modal.style.display = "none";
        }
    });
}