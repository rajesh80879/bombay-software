function themeToggle() {
    let element = document.body;
    if (count % 2 == 0) {
        element.setAttribute("data-layout-mode", "light");
        element.setAttribute("data-sidebar", "light");
    }
    else {
        element.setAttribute("data-layout-mode", "dark");
        element.setAttribute("data-sidebar", "dark");
    }
    count++
    localStorage.setItem("Count", count)
    console.log('count : ', count)
}

$(document).ready(function(){
    if (localStorage.Count) {
        count = localStorage.Count;
    }
    else {
        count = 0
        localStorage.setItem("Count", count)
    }
    let element = document.body;

    if (!element.hasAttribute("data-layout-mode")) {
        var att = document.createAttribute("data-layout-mode");
        element.setAttributeNode(att);
        att = document.createAttribute("data-sidebar");
        element.setAttributeNode(att);
    }

    if (count % 2 == 0) {
        element.setAttribute("data-layout-mode", "light");
        element.setAttribute("data-sidebar", "light");
    }
    else {
        element.setAttribute("data-layout-mode", "dark");
        element.setAttribute("data-sidebar", "dark");
    }
});