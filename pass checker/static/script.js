// ELEMENT REFERENCES

const passwordInput = document.getElementById("password")
const toggleBtn = document.getElementById("togglePassword")

const strengthBar = document.getElementById("strength-bar")
const strengthText = document.getElementById("strength-text")

const scoreText = document.getElementById("score")
const entropyText = document.getElementById("entropy")
const crackTimeText = document.getElementById("crack_time")

const feedbackList = document.getElementById("feedback-list")


// --------------------------------
// SHOW / HIDE PASSWORD
// --------------------------------

toggleBtn.addEventListener("click", () => {

    if(passwordInput.type === "password"){
        passwordInput.type = "text"
        toggleBtn.innerText = "🙈"
    } else {
        passwordInput.type = "password"
        toggleBtn.innerText = "👁"
    }

})


// --------------------------------
// PASSWORD INPUT EVENT
// --------------------------------

passwordInput.addEventListener("input", () => {

    const password = passwordInput.value

    if(password.length === 0){

        strengthBar.style.width = "0%"
        strengthText.innerText = "Waiting for input..."

        scoreText.innerText = "-"
        entropyText.innerText = "-"
        crackTimeText.innerText = "-"

        feedbackList.innerHTML = "<li>Start typing a password to analyze security</li>"

        return
    }

    analyzePassword(password)

})


// --------------------------------
// SEND PASSWORD TO FLASK API
// --------------------------------

function analyzePassword(password){

fetch("/analyze", {

method: "POST",

headers: {
"Content-Type": "application/json"
},

body: JSON.stringify({
password: password
})

})

.then(response => response.json())

.then(data => {

updateStrength(data.strength)

scoreText.innerText = data.score
entropyText.innerText = data.entropy + " bits"
crackTimeText.innerText = data.crack_time

updateFeedback(data.feedback)

})

.catch(error => {

console.error("Error:", error)

})

}


// --------------------------------
// STRENGTH BAR CONTROL
// --------------------------------

function updateStrength(strength){

let width = 0
let color = ""

switch(strength){

case "Very Weak":
width = 20
color = "#ff0033"
break

case "Weak":
width = 40
color = "#ff6600"
break

case "Medium":
width = 60
color = "#ffaa00"
break

case "Strong":
width = 80
color = "#00e676"
break

case "Very Strong":
width = 100
color = "#00ffff"
break

default:
width = 0
color = "gray"

}

strengthBar.style.width = width + "%"
strengthBar.style.background = color

strengthText.innerText = strength

}


// --------------------------------
// FEEDBACK LIST UPDATE
// --------------------------------

function updateFeedback(feedback){

feedbackList.innerHTML = ""

if(feedback.length === 0){

const li = document.createElement("li")
li.innerText = "✅ Excellent password security"

feedbackList.appendChild(li)

return
}

feedback.forEach(item => {

const li = document.createElement("li")

li.innerText = item

feedbackList.appendChild(li)

})

}


// --------------------------------
// OPTIONAL: ENTER KEY HANDLING
// --------------------------------

passwordInput.addEventListener("keypress", function(e){

if(e.key === "Enter"){
e.preventDefault()
}

})


// --------------------------------
// SMALL UI EFFECT
// --------------------------------

passwordInput.addEventListener("focus", () => {

passwordInput.style.boxShadow = "0 0 15px #00ffff"

})

passwordInput.addEventListener("blur", () => {

passwordInput.style.boxShadow = "none"

})