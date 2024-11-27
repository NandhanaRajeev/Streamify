// JavaScript to toggle between login and sign-up forms
document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("loginForm");
    const signUpForm = document.getElementById("signUpForm");
    const switchToSignUp = document.getElementById("switchToSignUp");
    const switchToLogin = document.getElementById("switchToLogin");

    // Show Login Form Initially
    loginForm.classList.add("active");

    // Switch to Sign Up
    switchToSignUp.addEventListener("click", (e) => {
        e.preventDefault();
        loginForm.classList.remove("active");
        signUpForm.classList.add("active");
    });

    // Switch to Login
    switchToLogin.addEventListener("click", (e) => {
        e.preventDefault();
        signUpForm.classList.remove("active");
        loginForm.classList.add("active");
    });
});