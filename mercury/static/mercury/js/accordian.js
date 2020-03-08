function myFunction() {
    text = document.getElementById("accordion-text");
    expand_more = document.getElementById("expand_more");
    expand_less = document.getElementById("expand_less");
    
    if (text.style.display == "block") {
        text.style.display = "none";
        expand_more.style.display = "block";
        expand_less.style.display = "none";
    }
    else {
        text.style.display = "block";
        expand_more.style.display = "none";
        expand_less.style.display = "block";
    }
  }

function displayForm() {
    text = document.getElementById("accordion-event-form");
    expand_more = document.getElementById("show_form");
    expand_less = document.getElementById("hide_form");
    
    if (text.style.display == "block") {
        text.style.display = "none";
        expand_more.style.display = "block";
        expand_less.style.display = "none";
    }
    else {
        text.style.display = "block";
        expand_more.style.display = "none";
        expand_less.style.display = "block";
    }
}