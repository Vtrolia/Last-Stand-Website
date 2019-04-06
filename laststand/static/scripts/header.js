
// set the onclick funxtion
window.addEventListener("load", () => {
    let options = document.querySelectorAll(".aside");
    for (let i = 0; i < options.length; i++) {
        options.item(i).setAttribute("onclick", 'redirect(this)');
    }
});

// hide menu if modal is clicked
document.addEventListener("click", (e) => {
    if(e.target.getAttribute("id") === "modal") {
        document.getElementById("hamburgerMenu").className = "reanimated";
        document.getElementById("modal").style.display = "none";
    }
});

// when a hamburger menu option is selected, send the user to that link
function redirect(selected) {
    let link = selected.getAttribute("data-link");
    window.location.replace("/" + link);
}

// change to dark picture
function changeSource(picture) {
    picture.setAttribute("src", dark_burger);
}

// change to light picture
function changeBack(picture) {
    picture.setAttribute("src", light_burger);
}

// show the hamburger menu if it is not shown, hide it if it is shown
function displayMenu() {
    var aside = document.getElementById("hamburgerMenu");

    if (aside.offsetWidth < (window.innerWidth * .01)) {
        aside.style.display = "block";
        document.getElementById("modal").style.display = "inherit";
        aside.className = "animated";
    }
    else {
        aside.className = "reanimated";
        document.getElementById("modal").style.display = "none";
    }
}