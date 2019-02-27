// all the changes from Last Stand Markdown into regular html
const staticVals = {
        "#b": "<strong>",
        "b#": "</strong>",
        "#it": "<em>",
        "it#": "</em>",
        "#lt": "<s>",
        "lt#": "</s>",
        "#sh": "<h4>",
        "sh#": "</h4>",
        "#j": "<span style=\"text-align: justify\>",
        "j#": "</span>",
        "#c": "<pre>",
        "c#": "</pre>",
        "#bl": "<ul>",
        "bl#": "</ul>",
        "#nl": "<ol>",
        "nl#": "</ol>",
        "#-": "<li>",
        "--#": "</li>",
        "#ta": "<table>",
        "ta#": "</table"
    };

// the class containing an article
class articlePost {
    constructor(text, title, date, author, image, imageTitle) {
        this.text = text;
        this.title = title;
        this.date = date;
        this.author = author;
        this.imageURL = image; 
        this.imageTitle = imageTitle;
    }

    // turn the article into an HTML nav, and add it to the document
    getHtmlObject() {
        let html = document.createElement("nav");
        html.className = "update";
        let h3 = document.createElement("h3");
        h3.textContent = this.title + " - " + this.date + " by " + this.author;
        html.append(h3);
        console.log(this.imageTitle);
        if(this.imageTitle != null && this.imageTitle != "") {
            let img = document.createElement("img");
            img.setAttribute("src", articleImageSrc + "/" + this.imageURL);
            img.setAttribute("title", this.imageTitle);
            html.append(img);
        }

        let p = document.createElement("p");
        p.innerHTML = articlePost.parse(this.text);
        html.append(p);
        
        // add the new object to the document
        document.getElementById("updates").appendChild(html);
    }
    
    // regular object
    getobj() {
        return {
            date: this.date,
            author: this.author,
            title: this.title,
            image_src: this.imageURL,
            image_title: this.imageTitle,
            content: this.text
        }
    }
    
    // json
    getJSON() {
        return {
            "date": this.date.toString(),
            "author": this.author.toString(),
            "title": this.title.toString(),
            "image_src": this.imageURL.toString(),
            "image_title": this.imageTitle.toString(),
            "content": this.text.toString()
        }
    }

    // change all the Last Stand Markdown into HTML
    static parse(text) {

        var final_text = text;
        
        // prevent XSS
        final_text = final_text.replace(/</g, "&lt;");
        final_text = final_text.replace(/>/g, "&gt;");
        
        // display newlines correctly
        final_text = text.replace(/\\\\r\\\\n/g, "<br>");
        
        // change each one by one
        var iterator = Object.keys(staticVals);
        for (let prop in iterator) {
            final_text = final_text.split(iterator[prop]).join(staticVals[iterator[prop]]);
        } 
        
        // justify entire text if that's what they selected
        if (final_text.substr(0, 9) === "&lt;j&gt;") {
            final_text = "<div align=\"justify\">" + final_text +
                         "</div>"
            final_text = final_text.split("&lt;j&gt;").join("");
        }

        return final_text;
    }
}

// this will be done when the page first loads, as well as when the user scrolls
function stories() {
    if ((window.innerHeight + Math.ceil(window.pageYOffset)) >= document.body.offsetHeight) {
        var request = new XMLHttpRequest();
        request.open("GET", "/get-articles");
        request.onload = () => {
            if (!request.responseText) {
                window.onscroll = undefined;
                return loadStory();

            }
            // for every article the server sent, make them into an html object then
            // add it to the articles field
            var reps = JSON.parse(request.responseText);
            for (let r in reps) {
                var article = new articlePost(reps[r]["content"], 
                                              reps[r]["title"], 
                                              reps[r]["date"], 
                                              reps[r]["author"], 
                                              reps[r]["image_src"], 
                                              reps[r]["image_title"]);
                article.getHtmlObject();
            }
        }
        request.send();
    }
}

// get more articles when the user scrolls to the bottom of the page
window.onscroll = stories;

// once the articles are all loaded, load the story at the bottom
function loadStory() {
    var story = new XMLHttpRequest();
    if (document.getElementById("storytime")) {
        return false;
    }
    story.open("POST", "/stories");
    story.setRequestHeader("X-CSRFToken", token)
    story.onload = () => {
        var newDiv = document.createElement("div");
        newDiv.setAttribute("id", "storytime");
        newDiv.className = "jumbotron";
        newDiv.innerHTML = story.responseText;
        document.body.appendChild(newDiv);
        document.getElementById("storytime").style.animationPlayState = "running";
    }
    story.send();
    
    // don't listen for any more scrolling
    window.onscroll = undefined;
}

window.onload = stories;