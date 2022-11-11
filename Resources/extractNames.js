displayText = ""

Array.from(document.getElementById("wolfermus").children).forEach(element => {
    child = element.children[2]
    if(child.children.length > 0) {
        displayText += `\n${child.children[0].innerHTML}`
    } else {
        displayText += `\n${child.innerHTML}`
    }
});

console.log(displayText)







displayText = ""

Array.from(document.getElementById("wolfermus").children).forEach(element => {
    child = element.children[0]
    if(child.children.length > 0) {
        displayText += `\n${child.children[0].innerHTML}`
    } else {
        displayText += `\n${child.innerHTML}`
    }
});

console.log(displayText)