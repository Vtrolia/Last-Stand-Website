
window.addEventListener("load", () => {
    let options = document.querySelectorAll(".aside");
    for (let i = 0; i < options.length; i++) {
        options.item(i).setAttribute("onclick", 'redirect(this)');
    }
});

document.addEventListener("click", (e) => {
    if(e.target.getAttribute("id") === "modal") {
        document.getElementById("hamburgerMenu").className = "reanimated";
        document.getElementById("modal").style.display = "none";
    }
});

function redirect(selected) {
    let link = selected.getAttribute("data-link");
    console.log(link)
    window.location.replace("/" + link);
}

function changeSource(picture) {
    picture.setAttribute("src", dark_burger);
}

function changeBack(picture) {
    picture.setAttribute("src", light_burger);
}

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