const emailInput      = document.getElementById("emailInput")
const passwordInput   = document.getElementById("passwordInput")
const toggleInputIcon = document.getElementById("toggleInput")
const loginButton     = document.getElementById("loginButton")
const errors          = document.getElementById("errors")

class LoginPage {
    constructor() {
        passwordInput.addEventListener("keyup", (event) => {
            if(event.code === "Enter" || event.code === "NumpadEnter"){
                this.submitForm()
            }
        })
        toggleInputIcon.addEventListener("click", () => this.showPassword())
        loginButton.addEventListener("click", () => this.submitForm())
    }

    showPassword() {
        toggleInputIcon.classList.toggle("ph-eye-slash")
        const inputType = passwordInput.getAttribute("type")
        passwordInput.setAttribute("type", inputType === "password" ? "text" : "password")
    }

    submitForm() {
        const email = emailInput.value
        const password = passwordInput.value
        if(email === "" || password === ""){
            return
        }
        this.setButtonLoading(true)

        login(email, password)
        .then(() => redirect('dashboard')) //Save credentials on LocalStorage
        .catch(error => {
            errors.innerText = error.message
            this.setButtonLoading(false)
        })
    }

    /** @param {boolean} loading */
    setButtonLoading(loading) {
        loginButton.innerHTML = loading
        ? "<div class=loader></div> Login"
        : "Login";
    }
}   

new LoginPage()
