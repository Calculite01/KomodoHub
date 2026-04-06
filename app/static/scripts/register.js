const passwordField = document.getElementById("password");
const confirmPasswordField = document.getElementById("confirm-password");
const passwordfeedback = document.getElementById("passwordfeedback");
const passwordfeedback2 = document.getElementById("passwordfeedback2");

const fnameField = document.getElementById("first-name");
const lnameField = document.getElementById("last-name");
const emailField = document.getElementById("Email");

const submitButton = document.getElementById("register-btn");

// Initial state
if (submitButton) submitButton.disabled = true;

document.addEventListener("input", () => {
    if (!submitButton) return; // Prevent errors if on OTP page

    const passwordStrength = passwordCheck();
    
    // Check if all fields are filled and password is strong
    const isFormInvalid = (
        fnameField.value.trim() === "" || 
        lnameField.value.trim() === "" || 
        emailField.value.trim() === "" || 
        passwordStrength < 3 || 
        passwordField.value !== confirmPasswordField.value ||
        confirmPasswordField.value === ""
    );

    if (isFormInvalid) {
        submitButton.disabled = true;
        submitButton.style.opacity = "0.6";
        submitButton.style.cursor = "not-allowed";
    } else {
        submitButton.disabled = false;
        submitButton.style.opacity = "1";
        submitButton.style.cursor = "pointer";
    }
});

function passwordCheck() {
    const password = passwordField.value;
    let strength = 0;

    // Reset feedback
    passwordfeedback.textContent = "";
    passwordfeedback.style.color = "#ef4444"; // Default Red

    if (password === "") {
        return 0;
    }

    if (password.length < 8) {
        passwordfeedback.textContent = "Password must be at least 8 characters.";
        return 0;
    }

    // Complexity check
    const regex = [/\d/, /[A-Za-z]/, /[^A-Za-z0-9]/];
    regex.forEach(re => {
        if (re.test(password)) strength++;
    });

    if (strength < 3) {
        passwordfeedback.textContent = "Include letters, numbers, and symbols.";
    } else {
        passwordfeedback.textContent = "Strong password!";
        passwordfeedback.style.color = "#228B22"; // Success Green
    }

    // Matching check
    if (confirmPasswordField.value !== "" && password !== confirmPasswordField.value) {
        passwordfeedback2.textContent = "Passwords do not match.";
        passwordfeedback2.style.color = "#ef4444";
    } else {
        passwordfeedback2.textContent = "";
    }

    return strength;
}