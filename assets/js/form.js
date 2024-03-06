let loginBtn = document.querySelector(".login-btn");
let signupBtn = document.querySelector(".signup-btn");

let loginForm = document.getElementById("login-form");
let signupForm = document.getElementById("signup-form");

console.log("Hello WOrld")

const login = () =>{
    loginForm.classList.remove("disabled");
    loginForm.classList.add("enabled");

    signupForm.classList.add("disabled");
    signupForm.classList.remove("enabled");

    loginBtn.classList.add("enabled");
    loginBtn.classList.remove("disabled");

    signupBtn.classList.remove("enabled");
    signupBtn.classList.add("disabled");
    localStorage.setItem("enabled", "login");
}

const signup = () =>{
    signupForm.classList.remove("disabled");
    signupForm.classList.add("enabled");

    loginForm.classList.add("disabled");
    loginForm.classList.remove("enabled");

    signupBtn.classList.add("enabled");
    signupBtn.classList.remove("disabled");

    loginBtn.classList.remove("enabled");
    loginBtn.classList.add("disabled");
    localStorage.setItem("enabled", "signup");
}

loginBtn.addEventListener("click", () => {
    login();
});

signupBtn.addEventListener("click", () => {
    signup();
});