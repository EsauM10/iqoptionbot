class Dashboard {
    constructor() {
        this.socket = io()
        const pages = [
            new HomePage(this.socket, "home", "ph ph-rocket-launch", true),
            new SettingsPage(this.socket, "settings", "ph ph-faders", false)
        ]
        
        this.socket.on("redirect", (pathname) => {redirect(pathname)})
        this.socket.on("pushNotification", (data) => this.pushNotification(data.message, data.type))
        this.socket.on("setAccountBalance", (accountBalance) => this.setAccountBalance(accountBalance))
        this.socket.on("setAccountMode", (accountMode) => this.setAccountMode(accountMode))

        this.sidebar = new Sidebar(pages)
        this.setPage(pages[0])
    }


    /**
     * @param {string} message 
     * @param {string} type 
     */
    pushNotification(message, type) {
        const messageDiv = document.querySelector(".message")
        messageDiv.innerHTML = `<p>${message}</p>`
        messageDiv.classList.add(type)
        document.querySelector(".notification").classList.add("received")
        
        setTimeout(() => {
            document.querySelector(".notification").classList.remove("received")
        }, 3000);
    }

    setPage(page) {
        page.render()
    }

    /** @param {number} value */
    setAccountBalance(value) {
        document.getElementById("accountBalance").innerText = `$ ${value}`
    }

    /** @param {string} accountMode */
    setAccountMode(accountMode) {
        document.getElementById("accountMode").innerText = accountMode === "PRACTICE" 
        ? "Conta de Treinamento" 
        : "Conta Real"
    }
}

new Dashboard()