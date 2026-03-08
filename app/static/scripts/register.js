const passwordField = document.getElementById("password");
const confirmPasswordField = document.getElementById("confirm-password");
const passwordfeedback = document.getElementById("passwordfeedback");
const passwordfeedback2 = document.getElementById("passwordfeedback2");

const fnameField = document.getElementById("first-name");
const lnameField = document.getElementById("last-name");

const emailField = document.getElementById("Email");

const submitButton = document.getElementById("register-btn");
submitButton.disabled = true;



document.addEventListener("input",event => {
    const passwordStrength = passwordCheck();
    console.log(passwordStrength);
    if (fnameField.value == "" || lnameField.value == "" || passwordStrength < 3 || emailField.value == "" || confirmPasswordField.value == ""){
    submitButton.disabled = true;
    }
    else{
        submitButton.disabled = false;
    }
})


function passwordCheck(){
    const password = passwordField.value;
    let strength = 0;
    if (password === ""){
        passwordfeedback.textContent = "";
        passwordfeedback2.textContent = "";
        return strength;
    }
    if (password.length < 8){
        passwordfeedback.textContent = "Password has to be atleast 8 characters";
        return strength;
    }
    const regex = [/\d/,/[A-Za-z]/,/[^A-Za-z0-9]/];
    for (const re of regex){
        if (re.test(password)){strength++;}
    }
    if (strength < 3){
        passwordfeedback.textContent = "Password must contain atleast one letter, one number, and one special character"; //Strength: Weak
        passwordfeedback2.textContent = "";
    }
    else{passwordfeedback.textContent = ""; passwordfeedback2.textContent = "";}//Strength: Strong
    return strength;
}