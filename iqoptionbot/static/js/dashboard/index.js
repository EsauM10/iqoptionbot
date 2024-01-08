class Dashboard {
    constructor() {
        this.socket = io()
        const pages = [
            new HomePage(this.socket, "home", "ph ph-rocket-launch", true),
            new SettingsPage(this.socket, "settings", "ph ph-faders", false)
        ]
        
        this.socket.on("redirect", (pathname) => {redirect(pathname)})
        this.socket.on("pushNotification", (data) => this.pushNotification(data.message, data.type))
        this.socket.on("setVersion", (version) => this.setVersion(version))

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

    /**
     * @param {string} version 
     */
    setVersion(version) {
        document.getElementById("version").innerText = `Versão: v${version}`
    }
}

new Dashboard()