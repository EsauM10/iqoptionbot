class Dashboard {
    constructor() {
        this.socket = io()
        const pages = [
            new HomePage(this.socket, "home", "ph ph-rocket-launch", true),
            new SettingsPage(this.socket, "settings", "ph ph-faders", false)
        ]
        
        this.socket.on("redirect", (pathname) => {
            console.log(pathname)
            redirect(pathname)
        })
        
        this.sidebar = new Sidebar(pages)
        this.setPage(pages[0])
    }

    setPage(page) {
        page.render()
    }
}

new Dashboard()